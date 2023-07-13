from tkinter import *
import xml.etree.ElementTree as ET
import re

root = Tk()
root.title("SOAP Converter")


def change_esql(form, myroot):
    ESQL = ""

    for parent in myroot:
        for child in parent:
            for child2 in child:
                for child3 in child2:
                    if re.split('}', child2.tag)[1] == 'Security':
                        continue
                    r = re.split('}', myroot.tag)[1]
                    p = re.split('}', parent.tag)[1]
                    c1 = re.split('}', child.tag)[1]
                    c2 = re.split('}', child2.tag)[1]
                    c3 = re.split('}', child3.tag)[1]
                    t = form[c3]

                    if t is None:
                        ESQL += f"SET OutputRoot.XMLNSC.xmlns:{r}.xmlns:{p}.xmlns:{c1}.xmlns:{c2}.xmlns:{c3}.(XML.Content) = NULL;\n"
                    else:
                        ESQL += f"SET OutputRoot.XMLNSC.xmlns:{r}.xmlns:{p}.xmlns:{c1}.xmlns:{c2}.xmlns:{c3} = '{t}';\n"

                    form[c3] = t

    return ESQL


def covert_to_esql(myroot):
    ESQL = ""
    form = {}

    for parent in myroot:
        for child in parent:
            for child2 in child:
                for child3 in child2:
                    if re.split('}', child2.tag)[1] == 'Security':
                        continue
                    r = re.split('}', myroot.tag)[1]
                    p = re.split('}', parent.tag)[1]
                    c1 = re.split('}', child.tag)[1]
                    c2 = re.split('}', child2.tag)[1]
                    c3 = re.split('}', child3.tag)[1]
                    t = child3.text

                    if t is None:
                        ESQL += f"SET OutputRoot.XMLNSC.xmlns:{r}.xmlns:{p}.xmlns:{c1}.xmlns:{c2}.xmlns:{c3} = '';\n"
                        # ESQL += f"SET OutputRoot.XMLNSC.xmlns:{r}.xmlns:{p}.xmlns:{c1}.xmlns:{c2}.xmlns:{c3}.(XML.Content) = NULL;\n"
                    else:
                        ESQL += f"SET OutputRoot.XMLNSC.xmlns:{r}.xmlns:{p}.xmlns:{c1}.xmlns:{c2}.xmlns:{c3} = '{t}';\n"

                    form[c3] = t

    return ESQL, form


def parse_xml():
    xml = xml_input.get("1.0", "end-1c")
    esql = esql_output.get("1.0", "end-1c")

    myroot = ET.fromstring(xml)
    ESQL, form = covert_to_esql(myroot)

    if esql != "":
        esql_output.delete("1.0", END)
    esql_output.insert(END, ESQL)

    [Label(root, text=f).grid(row=i + 4, column=0) for i, f in enumerate(form)]
    text_boxs = [Text(root, height=1, width=40) for f in enumerate(form)]
    keys = list(form.keys())

    for i, tb in enumerate(text_boxs):
        tb.grid(row=i + 4, column=2)
        text = form[keys[i]]

        if text != "":
            tb.delete("1.0", END)

        if text is None:
            tb.insert(END, "")
        else:
            tb.insert(END, text)

    def modify():
        for i, tb2 in enumerate(text_boxs):
            text2 = tb2.get("1.0", "end-1c")
            form[keys[i]] = text2

        ESQL2 = change_esql(form, myroot)
        esql = esql_output.get("1.0", "end-1c")

        if esql != "":
            esql_output.delete("1.0", END)
        esql_output.insert(END, ESQL2)

    button_modify = Button(root, text="Modify", command=modify)
    button_modify.grid(row=3, column=4)


label_input = Label(root, text="Input XML")
label_input.grid(row=0, column=0)
label_input = Label(root, text="Output ESQL")
label_input.grid(row=0, column=2)

xml_input = Text(root, height=5, width=40, bd=5)
xml_input.grid(row=1, column=0)
esql_output = Text(root, height=5, width=120, bd=5)
esql_output.grid(row=1, column=2)

sbv = Scrollbar(root, orient=VERTICAL)
sbh = Scrollbar(root, orient=HORIZONTAL)
sbv2 = Scrollbar(root, orient=VERTICAL)
sbh2 = Scrollbar(root, orient=HORIZONTAL)
sbv_main = Scrollbar(root, orient=VERTICAL)

sbv.grid(row=1, column=1, sticky=NS)
sbh.grid(row=2, column=0, sticky=EW)
sbv2.grid(row=1, column=3, sticky=NS)
sbh2.grid(row=2, column=2, sticky=EW)

xml_input.config(xscrollcommand=sbh.set, yscrollcommand=sbv.set, wrap=NONE)
esql_output.config(xscrollcommand=sbh2.set, yscrollcommand=sbv2.set, wrap=NONE)
sbv.config(command=xml_input.yview)
sbh.config(command=xml_input.xview)
sbv2.config(command=esql_output.yview)
sbh2.config(command=esql_output.xview)

button_convert = Button(root, text="Convert", command=parse_xml)
button_convert.grid(row=3, column=0)
button_exit = Button(root, text="Quit", command=root.quit)
button_exit.grid(row=3, column=2)

root.mainloop()
