import os


def get_pddl_domain_types(domain: str):
    start = domain.find("; Begin types\n") + len("; Begin types\n")
    end = domain.find("\n    ; End types", start)
    types = domain[start:end]
    return types


def get_pddl_domain_predicates(domain: str):
    start = domain.find("; Begin predicates\n") + len("; Begin predicates\n")
    end = domain.find("\n    ; End predicates", start)
    predicates = domain[start:end]
    return predicates


def get_pddl_domain_actions(domain: str):
    start = domain.find("; Begin actions\n") + len("; Begin actions\n")
    end = domain.find("\n    ; End actions", start)
    actions = domain[start:end]
    return actions


def get_pddl_problem_objects(problem: str):
    start = problem.find("; Begin objects\n") + len("; Begin objects\n")
    end = problem.find("\n    ; End objects", start)
    objects = problem[start:end]
    return objects


def get_pddl_problem_init(problem: str):
    start = problem.find("; Begin init\n") + len("; Begin init\n")
    end = problem.find("\n    ; End init", start)
    init = problem[start:end]
    return init


def set_pddl_problem_init(p_path: str, new_init: list):
    new_init_str = "\t\t" + "\n\t\t".join(new_init) + "\n"

    with open(p_path, 'r') as pf:
        content = pf.readlines()

    start_idx = content.index('    (:init\n') + 1
    end_idx = content.index('    ; End init\n') - 1
    content[start_idx:end_idx] = [new_init_str]

    with open(p_path, 'w') as pf:
        pf.writelines(content)


def get_pddl_problem_goal(problem: str):
    start = problem.find("; Begin goal\n") + len("; Begin goal\n")
    end = problem.find("\n    ; End goal", start)
    goal = problem[start:end]
    return goal


def set_pddl_problem_goal(p_path: str, new_goal: str):
    with open(p_path, 'r') as pf:
        content = pf.readlines()

    start_idx = content.index('    ; Begin goal\n') + 1
    end_idx = content.index('    ; End goal\n')
    content[start_idx:end_idx] = [new_goal]

    with open(p_path, 'w') as pf:
        pf.writelines(content)
