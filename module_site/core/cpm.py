import networkx as nx
from .component import Activity, Schedule, WorkType, ScheduleInformation


class CPM(nx.DiGraph):
    def __init__(self):
        super().__init__()
        self._make_span = -1

    # override
    def clear(self):
        self._make_span = -1

    # convert schedule to network
    def _worktype_to_activity(self, schedule_information):
        pass


    def _schedule_to_network(self, schedule):
        # TODO
        # add activity to network as node
        for act in schedule.activity_dict.values():
            self.add_node(act.id, act=act)
        # add dependency to network as edge
        for dep in schedule.dependency_list:
            self.add_edges_from([(dep[0], dep[1])])

    # critical path calculation
    def compute_critical_path(self, schedule):
        self.clear()
        self._schedule_to_network(schedule)
        self._update()
        schedule.critical_path = self._get_critical_path()

    def _forward(self):
        for n in nx.topological_sort(self):
            # TODO - add lagtime and relationship
            act = self.nodes[n]['act']
            ES = max([self.nodes[j]['act'].cpm_value_dict['EF'] for j in self.predecessors(n)], default=0)
            act.cpm_value_dict['ES'] = ES
            act.cpm_value_dict['EF'] = ES + act.duration
            # self.add_node(n, ES=ES, EF= ES + self.nodes[n]['act'].duration)

    def _backward(self):
        reversed_order = list(reversed(list(nx.topological_sort(self))))
        for n in reversed_order:
            # TODO - add lagtime and relationship
            act = self.nodes[n]['act']
            LF = min([self.nodes[j]['act'].cpm_value_dict['LS'] for j in self.successors(n)], default=self._make_span)
            act.cpm_value_dict['LF'] = LF
            act.cpm_value_dict['LS'] = LF - act.duration
            # self.add_node(n, LS=LF - self.nodes[n]['act'].duration, LF=LF)

    def _get_critical_path(self):
        G = set()
        for n in self:
            if self.nodes[n]['act'].cpm_value_dict['EF'] == self.nodes[n]['act'].cpm_value_dict['LF']:
                G.add(n)
        critical_path = self.subgraph(G)
        return critical_path
        # TODO - Float Calculation,

    # @property
    # def make_span(self):
    #     if not self._calculated:
    #         self._update()
    #     return self._make_span

    # @property
    # def criticalPath(self):
    #     if not self._calculated:
    #         self._update()
    #     return self._criticalPath

    def _update(self):
        self._forward()
        self._make_span = max([self.nodes[j]['act'].cpm_value_dict['EF'] for j in self.nodes], default=0)
        self._backward()
