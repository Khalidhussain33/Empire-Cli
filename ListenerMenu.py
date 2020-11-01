import shlex
import string
import textwrap

from prompt_toolkit.completion import Completion

import table_util
from EmpireCliState import state
from Menu import Menu
from utils import register_cli_commands, command


@register_cli_commands
class ListenerMenu(Menu):
    def __init__(self):
        super().__init__(display_name='listeners', selected='')

    def autocomplete(self):
        return self._cmd_registry + super().autocomplete()

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor()
        try:
            cmd_line = list(map(lambda s: s.lower(), shlex.split(document.current_line)))
            # print(cmd_line)
        except ValueError:
            pass
        else:
            if len(cmd_line) > 0 and cmd_line[0] in ['kill', 'info']:
                for listener in state.listeners.keys():
                    yield Completion(listener, start_position=-len(word_before_cursor))
            else:
                yield from super().get_completions(document, complete_event)

    def init(self):
        self.list()

    @command
    def list(self) -> None:
        """
        Get running/available listeners

        Usage: list
        """
        listener_list = list(map(lambda x: [x['ID'], x['name'], x['module'], x['listener_type'], x['created_at']],
                                 state.listeners.values()))
        listener_list.insert(0, ['ID', 'Name', 'Module', 'Listener Type', 'Created At'])

        table_util.print_table(listener_list, 'Listeners List')

    @command
    def info(self, listener_name: string) -> None:
        """
        Get details for the selected listener

        Usage: info <listener_name>
        """
        if listener_name not in state.listeners:
            return None

        listener_list = []

        for key, value in state.listeners[listener_name]['options'].items():
            values = list(map(lambda x: '\n'.join(textwrap.wrap(str(x), width=35)), value.values()))
            values.reverse()
            temp = [key] + values
            listener_list.append(temp)

        table_util.print_table(listener_list, listener_name)

    @command
    def kill(self, listener_name: string) -> None:
        """
        Kill the selected listener

        Usage: kill <listener_name>
        """
        state.kill_listener(listener_name)


listener_menu = ListenerMenu()
