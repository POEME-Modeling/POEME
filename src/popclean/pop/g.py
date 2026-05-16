# global lists the entire model needs

from .newton import Newton

element_list = list()
obs_list = list()
ind_list = list()
dep_list = list()
con_list = list()
state_list = list()
view_list = list()

solver = 0

VIDL = list()
x = 0.0
y = 0.0
name1 = "g"


# def __setattr__(self, name, value):
#     super().__setattr__(name, value)

#     if hasattr(self, name) and hasattr(getattr(self, name), "name1"):
#         temp = getattr(self, name)
#         temp.name1 = name


solve_state = "SS"


out = 0
win = 0
w = 0

output_file = open("test.out", "a")
NS = Newton("g.NS", output_file)

errors = "test"


def check():

    for e in element_list:
        e.precheck()

    for i in ind_list:
        i.precheck()

    for d in dep_list:
        d.precheck()

    for s in state_list:
        s.precheck()

    for c in con_list:
        c.precheck()


def set(var, value):

    stuff = element_list.copy()
    stuff.append(NS)

    for e in stuff:
        for v in e.VIDL:
            if v.name1 == var:
                v.v = value
            if v.VIDL != 0:
                for v1 in v.VIDL:
                    if v1.name1 == var:
                        v1.v = value
                    try:
                        for v2 in v1.VIDL():
                            if v2.name1 == var:
                                v2.v = value

                    except:  # noqa: E722, S110
                        pass
