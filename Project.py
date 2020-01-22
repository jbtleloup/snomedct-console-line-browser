class ConceptSimplified:
    def __init__(self, concept_id):
        self.groups = ['0']
        self.relationships = []
        self.children = []
        self.parents = []
        self.FSN = "None"
        self.concept_id = concept_id

    def display_info(self):
        print("id: " + self.concept_id, "FSN: " + self.FSN, "#Parents: " + str(len(self.parents)),
              "#Rels: " + str(len(self.relationships)), "#groups: " + str(max(self.groups)))

    def __str__(self):
        output = "Concept id: " + self.concept_id + " "
        output += "FNS: " + self.FSN + " "
        output += "Parents: " + ", ".join(self.parents) + " "
        output += "Children: " + ", ".join(self.children) + " "
        output += "Relationship: " + ", ".join(self.relationships) + " "
        output += "Groups: " + ", ".join(self.groups) + " "

        return output


def display_concept_children_information(concepts, concept_id):
    try:
        main_concept = concepts[concept_id]
    except KeyError:
        print("The concept related to this key could not be found... Please, verify that the key is correct.")
    else:
        main_concept.display_info()
        for child in main_concept.children:
            display_concept_children_information(concepts, child)


def initialize_id_in_concepts(concepts):
    i = 0
    with open('files/Concept.txt') as f1:
        for l in f1:
            if i == 0:
                i += 1
            else:
                line = l.strip().split("\t")
                if line[2] == '1':
                    new_concept = ConceptSimplified(line[0])
                    concepts[new_concept.concept_id] = new_concept


def initalize_FSN_in_concepts(concepts):
    i = 0
    with open('files/Description.txt') as f2:
        for l in f2:
            if i == 0:
                i += 1
            else:
                line = l.strip().split("\t")
                if line[2] == '1' and line[6] == "900000000000003001" and line[4] in concepts:
                    concepts[line[4]].FSN = line[7]


def initialize_relationships_in_concepts(concepts):
    i = 0
    with open('files/Relationship.txt') as f3:
        for l in f3:
            if i == 0:
                i += 1
            else:
                line = l.strip().split("\t")
                if line[2] == '1':
                    if line[7] == "116680003":  # = is a ...
                        concepts[line[4]].parents.append(line[5])  # Child
                        concepts[line[5]].children.append(line[4])  # Parent
                    else:
                        concepts[line[4]].relationships.append(line[5])  # Relationship
                        concepts[line[4]].groups.append(line[6])  # Groups


def show_welcome_message():
    print("**********************************************************")
    print("|                                                        |")
    print("|        WELCOME TO SNOMED CT BROWSER FOR TERMINAL       |")
    print("|  author: Jean-Baptiste Tamas-Leloup github: jbtleloup  |")
    print("|                                                        |")
    print("**********************************************************")


def main():
    # hash table of objects of type ConceptSimplified
    concepts = {}

    # wrapper function - read files to initialize required attributes
    # for each ConceptSimplified in concepts
    initialize_concepts_wrapper(concepts)

    # export content of concepts in a file 'output'
    writing_concepts_in_output_file(concepts)

    show_welcome_message()

    while 1:
        concept_id = ask_concept_id_from_user()
        display_concept_children_information(concepts, concept_id)


def writing_concepts_in_output_file(concepts):
    print("WRITING IN OUTPUT FILE")
    file = open('output', 'w')
    for x in concepts:
        file.write(concepts[x].__str__() + "\n")
    file.close()


def initialize_concepts_wrapper(concepts):
    # read Concept.txt file
    print("READING Concept.txt")
    initialize_id_in_concepts(concepts)
    # Read Description.txt file
    print("READING Description.txt")
    initalize_FSN_in_concepts(concepts)
    # Read Relationship.txt
    print("READING Relationship.txt")
    initialize_relationships_in_concepts(concepts)


def ask_concept_id_from_user():
    print("Please, enter the id of the concept you would like to visualize")
    try:
        concept_id_from_user = int(input("-> "))
    except ValueError:
        print("Id needs to be a number")
        concept_id_from_user = ask_concept_id_from_user()
    return str(concept_id_from_user)


if __name__ == '__main__':
    main()
