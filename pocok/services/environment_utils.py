import os
import sys
from subprocess import Popen, PIPE
from .console_logger import ColorPrint


class EnvironmentUtils:

    @staticmethod
    def get_variable(key, default=None):
        return os.environ.get(key, default)

    @staticmethod
    def check_docker():
        p = Popen("docker version -f {{.Server.Version}}", stdout=PIPE, stderr=PIPE, shell=True)
        out, err = p.communicate()
        if not len(err) == 0 or len(out) == 0:
            ColorPrint.exit_after_print_messages(message='Docker not running.')
        if str(out).split(".")[0] < str(17):
            ColorPrint.exit_after_print_messages(message='Please upgrade Docker to version 17 or above')

    @staticmethod
    def check_kubernetes():
        p = Popen("kubectl version --short", stdout=PIPE, stderr=PIPE, shell=True)
        out, err = p.communicate()
        if not len(err) == 0 or len(out) == 0:
            ColorPrint.exit_after_print_messages(message=str(err).strip())
        ColorPrint.print_with_lvl(message="Kubernetes\n " + str(out).strip())

    @staticmethod
    def check_helm():
        p = Popen("helm version -s --short", stdout=PIPE, stderr=PIPE, shell=True)
        out, err = p.communicate()
        if not len(err) == 0 or len(out) == 0:
            ColorPrint.exit_after_print_messages(message=str(err).strip())
        ColorPrint.print_with_lvl(message="Helm\n " + str(out).strip(), lvl=1)

    @staticmethod
    def check_version(version):

        newest_version = "0.0.0"

        # check pip
        p = Popen("pip install pocok==", stdout=PIPE, stderr=PIPE, shell=True)
        out, err = p.communicate()
        if not len(err) == 0:
            newest_version = EnvironmentUtils.parse_version(str(err))
        else:
            # maybe installed from source
            return
        if version < newest_version:
            ColorPrint.print_warning("New version of pocok is available (%r). \n "
                                     "Please upgrade with: pip install -U pocok" % newest_version)

    @staticmethod
    def parse_version(pip_content):
        if "(from versions: " in pip_content:
            first_line = pip_content.strip().splitlines()[0]
            versions = first_line.split(",")
            if not len(versions[-1]) == len(first_line):
                return versions[-1].strip(') ')
        return "0.0.0"

    @staticmethod
    def decode(text_string):
        if sys.version_info[0] == 3:
            return text_string.decode("utf-8")
        return text_string
