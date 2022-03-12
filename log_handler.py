#  ler o log com pyparsing?
from time import strftime
import common as cm
from os import path


class Logger:
    def __init__(self):
        self.log_dir = cm.resource_path("LogFile.log")

    def log_it(self, facility, severity_level, message):
        """Set a string in log pattern and save to c.log file.
        Facility: kern, user, mail, daemon, auth, syslog, lpr, news, security, console...
        Severity level: emerg, alert, crit, err, warning, notice, info and debug.
        https://en.wikipedia.org/wiki/Syslog"""
        time_stamp = strftime("%Y-%m-%d %H:%M:%S")
        _pattern = f"<{severity_level}> {time_stamp} {facility}: {message}"
        self.save_log(_pattern)

    def save_log(self, line):
        """Create a log file with header and a new line or add another line to the current
        log file."""
        time_stamp = strftime("%Y-%m-%d %H:%M:%S")
        if path.isfile(self.log_dir):
            with open(self.log_dir, "a") as file:
                file.write(f"\n{line}")
        else:
            with open(self.log_dir, "a") as file:
                file.write(
                    f"# Constancy\n# Version: 2.0\n# Log file creation date: {time_stamp}\n"
                    f"# <severity-level> time-stamp facility.User: message\n{line}"
                )


def main():
    Logger()


if __name__ == "__main__":
    main()
