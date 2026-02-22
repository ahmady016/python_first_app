##############################################################################
from datetime import datetime
from rich.console import Console    # pyright: ignore[reportMissingImports]
from icecream import ic   # pyright: ignore[reportMissingImports]
##############################################################################
# configure icecream to work with rich console and add timestamp prefix to each log
# and also clean the output to remove the label and variable name
# from the output and only print the value
def icecream_config():
    # create a rich console instance
    console = Console()

    # function to clean the output
    def clean_rich_printer(s):
        # check if the string contains an f-string pattern and remove it
        if 'f"' in s:
            start = s.find('f"')
            end = s.find('": ', start + 2)
            if end != -1:
                console.print(s.replace(s[start:end+3], ""))
        # check if the string contains a pattern like 'variable: value'
        # and remove the variable name
        elif ': ' in s:
            start = s.find('-> ')
            end = s.find(': ')
            console.print(s.replace(s[start+2:end+1], ""))
        # if the string does not contain any pattern, print it as is
        else:
            console.print(s)

    # function to generate the timestamp prefix for icecream logs
    def time_prefix():
        return f'{datetime.now()} -> '

    # configure icecream to use the custom prefix and output function
    ic.configureOutput(prefix=time_prefix, outputFunction=clean_rich_printer)


if __name__ == "__main__":
    icecream_config()
    ic("Icecream Configured Successfully")
