from copy import deepcopy


def export_result(response: str, file_name: str):
    if "```" in response:
        response = response.split("```")[1]
    start_idx = response.find("(define")
    if start_idx != 0 and response[0: start_idx] != "\n":
        response = response.replace(response[0: start_idx], "")
    with open(file_name, "w") as f:
        f.write(response)


def export_obj_list(response: str):
    assert "[" in response and "]" in response, "No list found in response!"
    start_idx = response.find("[")
    end_idx = response.rfind("]")

    obj_list_str = response[start_idx + 1:end_idx]
    return eval(obj_list_str)


def export_subgoal_list(response: str):
    subgoal_list = []
    for g in response.split("```"):
        cg = deepcopy(g)
        cg = cg.replace(" ", "")
        if "(:goal" in cg and cg.endswith(")\n"):
            subgoal_list.append(g[g.find("(:goal"):g.rfind(")\n")+len(")\n")])
    return subgoal_list


def export_sayplan_search_cmd(response: str):
    start_idx = response.find("{")
    end_idx = response.find("}")
    sliced_response = response[start_idx:end_idx+1]
    output = eval(sliced_response)
    return output["mode"], output["chain_of_thought"], output["reasoning"], output["command"]


def export_sayplan_plan(response: str, file_name: str):
    start_idx = response.find("{")
    end_idx = response.find("}")
    response = eval(response[start_idx:end_idx+1])
    plan = response["plan"]
    if "```" in plan:
        plan = plan.split("```")[1]
    if "\\n" in plan:
        plan = plan.replace("\\n", "\n")
    response_lines = plan.split("\n")
    plan_list = [line[line.find("("):]
                 for line in response_lines if line.strip() != ""]
    plan_length = len(plan_list)
    with open(file_name, "w") as f:
        f.write("\n".join(plan_list))
    return plan_list, plan_length


def export_python_code(response: str):
    start_idx = response.find("```python")
    end_idx = response.rfind("```")
    return response[start_idx + len("```python"): end_idx]
