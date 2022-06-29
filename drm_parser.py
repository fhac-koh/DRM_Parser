class parser:
    def __init__(self):
        self.classify_number = ["21", "22", "46"]

    def file_open(self, path):
        drm_file = open(path)
        contents = drm_file.read()
        return contents.splitlines()

    def detective_classify_id(self, text_lines):
        contents = []
        for line in text_lines:
            if (line[0:2] in self.classify_number):
                contents.append(line)
        return contents

    def parse(self, text_lines):
        nodes = []
        links = []
        locates = []
        for line in text_lines:
            result = self.parse_line(line)
            if result[0] == "node":
                nodes.append(result[1:])
            elif result[0] == "link":
                continue_flag = result[1][0]
                if continue_flag:
                    links[len(links)-1][1].extend(result[1][2])
                else:
                    links.append(result[1][1:])
            elif result[0] == "locate":
                locates.append(result[1:])
        return nodes, links, locates

    def parse_line(self, text_line):
        recode_id = text_line[0:2]
        if recode_id == "21":
            label = "node"
            return label, self.parse_node(text_line)
        elif recode_id == "22":
            label = "link"
            return label, self.parse_link(text_line)
        elif recode_id == "46":
            label = "locate"
            return label, self.parse_locate(text_line)
        else:
            print("illegal line:", text_line)

    def parse_node(self, text_line):
        node_id = text_line[2:6]
        axis = [int(text_line[8:13]), int(text_line[13:18])]
        link_list = []
        link_from_begin = 33
        link_to_end = 48
        diff = link_to_end - link_from_begin
        for i in range(8):
            link = int(text_line[link_from_begin + diff*i:link_to_end + diff*i])
            link_list.append(link)
        return int(node_id), axis, link_list

    def parse_link(self, text_line):
        continue_flag = False if text_line[10:12] == "01" else True
        linked_node_id = [int(text_line[2:6]), int(text_line[6:10])]
        axis_list = []
        axis_from_begin = 91
        axis_to_end = 101
        diff = axis_to_end - axis_from_begin
        for i in range(16):
            axis = text_line[axis_from_begin + diff*i:axis_to_end + diff*i]
            if (axis != "0000000000"):
                axis_list.append([int(axis[:5]), int(axis[5:])])
        return continue_flag, linked_node_id, axis_list

    def parse_locate(self, text_line):
        axis = [int(text_line[23:28]), int(text_line[28:33])]
        display_name = text_line[35:45].rsplit("00")[0]
        official_name = text_line[79:109].rsplit("00")[0]
        return axis, display_name, official_name
