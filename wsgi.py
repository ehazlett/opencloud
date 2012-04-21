import application
import newrelic.agent
app = application.app

newrelic.agent.initialize('newrelic.ini')
app = newrelic.agent.wsgi_application()(app)
