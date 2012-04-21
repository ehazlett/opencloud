import application
import newrelic.agent
app = application.app

newrelic.agent.initialize('newrelic.ini', 'development')
app = newrelic.agent.wsgi_application()(app)
