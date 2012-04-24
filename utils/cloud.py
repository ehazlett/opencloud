#!/usr/bin/env python
#    Copyright 2012 OpenCloud Project
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.deployment import ScriptDeployment
import libcloud.security
from celery.task import task
from flaskext.cache import Cache
from utils.logger import get_logger
import config

libcloud.security.VERIFY_SSL_CERT = config.LIBCLOUD_VERIFY_CERTS

app = config.create_app()
cache = Cache(app)

def _get_connection(provider=None, region=None, id=None, key=None):
    """
    Gets a libcloud connection to the specified provider
    
    :param provider: Name of provider (i.e. ec2)
    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key
    
    """
    regions = {
        'ec2': Provider.EC2,
        'us-east-1': Provider.EC2_US_EAST,
        'us-west-1': Provider.EC2_US_WEST,
        'us-west-2': Provider.EC2_US_WEST_OREGON,
        'eu-west-1': Provider.EC2_EU_WEST,
        'rackspace': Provider.RACKSPACE,
        'rackspace_uk': Provider.RACKSPACE_UK,
        'dfw': Provider.RACKSPACE,
    }
    driver = get_driver(regions[region.lower()])
    conn = driver(id, key)
    return conn

def get_nodes(provider=None, region=None, id=None, key=None, node_ids=None):
    """
    List all nodes for the specified provider

    :param provider: Name of provider (i.e. ec2)
    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key
    :param node_ids: List of node IDs to filter

    :rtype: `list` of nodes

    """
    nodes = None
    if node_ids and not isinstance(node_ids, list):
        nodes_ids = [node_ids]
    conn = _get_connection(provider, region, id, key)
    if provider == 'ec2':
        nodes = conn.list_nodes(node_ids)
    else:
        nodes = conn.list_nodes()
    return nodes

def reboot_node(provider=None, region=None, id=None, key=None, node_id=None):
    """
    Reboots an instance

    :param provider: Name of provider (i.e. ec2)
    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key
    :param node_id: ID of the node to restart
    
    """
    log = get_logger(__name__)
    log.info('Restarting instance {0}'.format(node_id))
    node = get_nodes(provider, region, id, key, [node_id])[0]
    ret_val = None
    # check if node is stopped ; run start instead of reboot
    if node.state == 4:
        ret_val = node.driver.ex_start_node(node)
    else:
        ret_val = node.reboot()
    return ret_val

def stop_node(provider=None, region=None, id=None, key=None, node_id=None):
    """
    Stops an instance

    :param provider: Name of provider (i.e. ec2)
    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key
    :param node_id: ID of the node to restart

    """
    log = get_logger(__name__)
    log.info('Stopping instance {0}'.format(node_id))
    node = get_nodes(provider, region, id, key, [node_id])[0]
    ret_val = False
    # only ec2 can 'stop' nodes
    ret_val = node.driver.ex_stop_node(node)
    return ret_val

def destroy_node(provider=None, region=None, id=None, key=None, node_id=None):
    """
    Destroys an instance

    :param provider: Name of provider (i.e. ec2)
    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key
    :param node_id: ID of the node to restart

    """
    log = get_logger(__name__)
    log.info('Destroying instance {0}'.format(node_id))
    node = get_nodes(provider, region, id, key, [node_id])[0]
    return node.destroy()

@cache.memoize(3600)
def _get_ec2_images(region=None, id=None, key=None):
    """
    Gets all Amazon EC2 images
    
    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key

    :rtype: `list` of images

    """
    conn = _get_connection('ec2', region, id, key)
    images = []
    [images.append({'name': x.name, 'id': x.id}) for x in conn.list_images(region)]
    return images

@cache.memoize(3600)
def _get_rackspace_images(region=None, id=None, key=None):
    """
    Gets all Rackspace images

    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key

    :rtype: `list` of images

    """
    conn = _get_connection('rackspace', region, id, key)
    images = []
    [images.append({'name': x.name, 'id': x.id}) for x in conn.list_images()]
    return images

def get_images(provider=None, region=None, id=None, key=None):
    """
    List all images for the specified provider

    :param provider: Name of provider (i.e. ec2)
    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key

    :rtype: `list` of images

    """
    images = {
        'ec2': _get_ec2_images,
        'rackspace': _get_rackspace_images,
    }
    return images[provider](region, id, key)

def get_sizes(provider=None, region=None, id=None, key=None):
    """
    List all sizes for the specified provider

    :param provider: Name of provider (i.e. ec2)
    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key

    :rtype: `list` of sizes

    """
    sizes = {
        'ec2': _get_ec2_sizes,
        'rackspace': _get_rackspace_sizes,
    }
    return sizes[provider](region, id, key)

@cache.memoize(3600)
def _get_ec2_sizes(region=None, id=None, key=None):
    """
    Gets all EC2 sizes

    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key

    :rtype: `list` of sizes

    """
    conn = _get_connection('ec2', region, id, key)
    sizes = []
    [sizes.append({'name': x.name, 'id': x.id}) for x in conn.list_sizes()]
    return sizes

@cache.memoize(3600)
def _get_rackspace_sizes(region=None, id=None, key=None):
    """
    Gets all Rackspace sizes

    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key

    :rtype: `list` of images

    """
    conn = _get_connection('rackspace', region, id, key)
    sizes = []
    [sizes.append({'name': x.name, 'id': x.id}) for x in conn.list_sizes()]
    return sizes
    
@task
def launch_node(provider=None, region=None, id=None, key=None, name=None, image_id=None, size_id=None, \
    **kwargs):
    """
    Launches a new node for the specified provider

    :param provider: Name of provider (i.e. ec2)
    :param region: Name of region
    :param id: Provider ID 
    :param key: Provider Key
    :param name: Name of instance
    :param image_id: ID of image to use
    :param size_id: ID of size to use
    :param kwargs: Miscellaneous provider specific args

    """
    log = get_logger(__name__)
    log.debug('Launching a new node in {0}, region {1}: Image: {2} Size: {3}'.format(provider, \
        region, image_id, size_id))
    conn = _get_connection(provider, region, id, key)
    image = [x for x in conn.list_images() if x.id == image_id]
    size = [x for x in conn.list_sizes() if x.id == size_id]
    if image:
        image = image[0]
    if size:
        size = size[0]
    if not image or not size:
        raise ValueError('Invalid image_id or size_id')
    if provider == 'ec2':
        keypair = kwargs.get('keypair', None)
        security_groups = kwargs.get('security_groups', [])
        if not isinstance(security_groups, list):
            security_groups = security_groups.split()
        node = conn.create_node(name=name, image=image, size=size, ex_keyname=keypair, ex_securitygroup=security_groups)
    else:
        node = conn.create_node(name=name, image=image, size=size, )
    msg = "Node launched: {0} ({1}) in {2} region of {3} ; {4}".format(node.name, node.uuid, region, provider, \
        node.extra)
    log.info(msg)
    return msg
    