import os
from pkg_resources import parse_version as version
import reframe as rfm
import reframe.utility.sanity as sn
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from tools_list import tools, standard_partitions_tool_test

@rfm.simple_test
class VSCToolAvailabilityTest(rfm.RunOnlyRegressionTest):
    tool = parameter(tools.keys())

    valid_prog_environs = ["standard"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    maintainers = ["smoors", "Lewih"]
    tags = {"vsc", "cue", "tools"}

    def __init__(self):
        
        if 'avail_on' in tools[self.tool].keys():
            self.valid_systems = []
            for x in tools[self.tool]['avail_on']:
                self.valid_systems += [f'{x}']
        else:
            self.valid_systems = standard_partitions_tool_test

        self.not_as_module = tools[self.tool].get('not_as_module')

    @run_after('init')
    def set_param(self):
        self.executable = f"""command -v {tools[self.tool]['exe']}"""
        
        modname = tools[self.tool].get('modname')
        if modname and not self.not_as_module:
            self.modules = [modname]
        if modname and self.not_as_module:
            self.postrun_cmds = [f'ml spider {modname}']

    @deferrable
    def my_finder(self, patt, string):
        # Cleaning up job prolog message in the Slurm job output file specific to KU Leuven site
        prolog_cleanup = ''
        with open(string, 'r') as fh:
            lines = list(fh)
            if lines:
                prolog_cleanup = [_ for _ in lines if not (_.startswith('SLURM_') or
                                                           'Date' in _ or
                                                           'Walltime' in _ or
                                                           _.startswith('==='))]
                prolog_cleanup = ''.join(prolog_cleanup)
        
        num_matches = sn.count(sn.finditer_s(patt, prolog_cleanup))

        return True if num_matches > 0 else False

    @sanity_function
    def assert_availability(self):
        if self.not_as_module:
            out = sn.and_(self.my_finder(r'^[a-zA-Z/]', self.stdout),
                          self.my_finder(r'Unable to find', self.stderr))
        else:
            out = self.my_finder(r'^[a-zA-Z/]', self.stdout)

        if tools[self.tool].get('negate'):
            return sn.not_(out)
        else:
            return out


@rfm.simple_test
class VSCToolVersionTest(rfm.RunOnlyRegressionTest):

    targets = []
    for x in tools.keys():
        if 'minver' in tools[x].keys():
            targets += [x]
    tool = parameter(targets)

    valid_prog_environs = ["standard"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    maintainers = ["smoors", "Lewih"]
    tags = {"vsc", "cue", "tools"}

    def __init__(self):

        if 'avail_on' in tools[self.tool].keys():
            self.valid_systems = []
            for x in tools[self.tool]['avail_on']:
                self.valid_systems += [f'{x}']
        else:
            self.valid_systems = standard_partitions_tool_test

    @run_after('init')
    def set_param(self):
        ## dependency between tests
        variant = VSCToolAvailabilityTest.get_variant_nums(tool=lambda x: x==self.tool)
        self.depends_on(VSCToolAvailabilityTest.variant_name(variant[0]))

        self.descr = f"version >= {tools[self.tool]['minver']}"
        self.executable = f"""python3 version_check.py '{json.dumps(tools[self.tool])}' """
        modname = tools[self.tool].get('modname')
        if modname:
            self.modules = [modname]

    @sanity_function
    def assert_availability(self):
        return sn.assert_found(r'^True$', self.stdout)

