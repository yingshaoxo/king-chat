#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python, Terminal
py = Python()
t = Terminal()

class Tools():
    def __clear(self):
        commands = """
sudo rm -fr king_chat.egg-info
sudo rm -fr dist
sudo rm -fr build
        """
        t.run(commands)

    def work(self, on_what):
        if on_what == "client":
            t.run_program("terminator -e 'vim king_chat/client.py'")
        elif on_what == "server":
            t.run_program("terminator -e 'vim king_chat/server.py'")

    def push(self, comment):
        self.__clear()

        t.run('git add .')
        t.run('git commit -m "{}"'.format(comment))
        t.run('git push origin')

    def pull(self):
        t.run("""
git fetch --all
git reset --hard origin/master
""")

    def install(self):
        self.__clear()
        t.run("""
sudo -H python3 setup.py sdist bdist_wheel

cd dist
sudo pip3 uninstall -y king_chat
sudo pip3 install king_chat*

cd ..
        """)
        self.__clear()

    def publish(self):
        self.install()
        t.run("""
twine upload dist/*
        """)
        self.__clear()


py.make_it_runnable()
py.fire(Tools)
