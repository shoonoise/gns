import cherrypy

from chrpc.server import Module
from .. import service

from . import jobs
from . import rules
from . import state
from . import golem


##### Public methods #####
def run(config):
    (root, server_opts) = _init(config, service.S_CHERRY)
    if not config[service.S_CORE][service.O_HANDLE_SIGNALS]:
        del cherrypy.engine.signal_handler
    cherrypy.quickstart(root, config=server_opts)

def make_wsgi_app():
    config = service.init(description="GNS HTTP API")[0]
    (root, server_opts) = _init(config, service.S_API)
    cherrypy.tree.mount(root, "/", server_opts)
    return cherrypy.tree


##### Private methods #####
def _make_tree(config):
    root = Module()
    root.api = Module()

    root.api.rest = Module()
    root.api.rest.v1 = Module()
    root.api.rest.v1.jobs = jobs.JobsResource(config)
    root.api.rest.v1.rules = Module()
    root.api.rest.v1.rules.head = rules.HeadResource(config)
    root.api.rest.v1.system = Module()
    root.api.rest.v1.system.state = state.StateResource(config)

    root.api.compat = Module()
    root.api.compat.golem = Module()
    root.api.compat.golem.submit = golem.SubmitApi(config)

    disp_dict = { "request.dispatch": cherrypy.dispatch.MethodDispatcher() }
    return (root, { path: disp_dict for path in (
                "/api/rest/v1/jobs",
                "/api/rest/v1/rules/head",
                "/api/rest/v1/system/state",
                "/api/compat/golem/submit",
            )
        })

def _init(config, section):
    (root, app_opts) = _make_tree(config)
    server_opts = config[section].copy()
    server_opts.update(app_opts)
    return (root, server_opts)
