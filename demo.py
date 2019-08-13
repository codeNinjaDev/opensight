import uvicorn
from starlette.testclient import TestClient

from hbll.backend import Program
from hbll.backend.manager_schema import ModulePath
from hbll.webserver import WebServer


def make_program():
    program = Program()
    program.manager.register_module(ModulePath("modules", "seven"))

    program.manager.register_module(ModulePath("modules", "six"))
    program.manager.register_module(ModulePath("modules", "five"))

    return program


def make_nodetree(program):
    func_type = "demo.five/Five"
    node = program.create_node(func_type)

    func_type = "demo.five/Sum"
    node = program.create_node(func_type)


def test_webserver(webserver):
    print()
    print(webserver.get_funcs())
    print()
    print(webserver.get_nodes())
    print()


def main():
    program = make_program()

    make_nodetree(program)

    webserver = WebServer(program)

    test_webserver(webserver)

    uvicorn.run(webserver.app)


if __name__ == "__main__":
    main()
