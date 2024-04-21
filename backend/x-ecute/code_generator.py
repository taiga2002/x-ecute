def main(lst):
    animations = {
        "rocket": 0,
        "heart": 1
    }
    output = {
        "reword": "",
        "display": True,
        "animation": -1
    }
    for func in lst:
        split = func.split('.')
        if split[0] == "reword" and output["reword"] == "":
            output["reword"] = split[1]
        if split[0] == "animate" and output["animation"] == -1:
            output["animation"] = animations[split[1]]
        if split[0] == "display":
            output["display"] = False
    return output

# [animate.heart, display.hide, animate.rocket] => 
# {"reword": "", "display": False, "animation": 1}