class Person:
    def __init__(self, name, age, infected_status, vaccines):
        self.name = name
        self.age = age
        self.infected_status = infected_status
        self.living_status = True
        self.vaccines = vaccines
        self.down = []
        self.parent = None

    def add_down(self, Person):
        self.down.append(Person)
        Person.parent = self

    def spread_virus(self):
        # print(f"Infection avant propagation pour {self.name}: {self.infected_status}")
        list_variant = [2, 3, 5, 7, 11]
        status_below = 1
        if self.infected_status % 7 == 0 and not self.vaccines and self.living_status:
            one_on_two = 1
            for people in self.parent.down:
                if people.infected_status % 7 != 0 and one_on_two == 1 and not people.vaccines:
                    people.infected_status *= 7
                one_on_two *= -1

        for element in self.down:
            element.infected_status *= infect_a(self, element)
            element.infected_status *= infect_32_down(self, element)
            infected = element.spread_virus()
            for variant in list_variant:
                if infected % variant == 0 and status_below % variant != 0:
                    status_below *= variant

        self.infected_status *= infect_b(status_below, self)
        self.infected_status *= infect_32_up(status_below, self)
        self.infected_status *= infect_ultime(status_below, self)
        if self.vaccines and self.infected_status % 2 == 0:
            self.infected_status /= 2
        if self.vaccines and self.infected_status % 5 == 0:
            self.infected_status /= 5
        # print(f"Infection après propagation pour {self.name}: {self.infected_status}")
        return self.infected_status if self.living_status else 1

    def vaccin_a1(self):
        for element in self.down:
            if (element.infected_status % 2 == 0 or element.infected_status % 5 == 0) and 0 <= element.age <= 30:
                element.infected_status = 1
                element.vaccines = True
            element.vaccin_a1()

    def vaccin_b1(self):
        one_on_two = 1
        for element in self.down:
            if (element.infected_status % 3 == 0 or element.infected_status % 7 == 0) and element.living_status:
                if one_on_two == 1:
                    element.infected_status = 1
                else:
                    element.living_status = False
                one_on_two *= -1
            element.vaccin_b1()

    def vaccin_ultime(self):
        for element in self.down:
            if element.infected_status % 11 == 0:
                element.infected_status = 1
                element.vaccines = True
            element.vaccin_ultime()

    def print_info(self, indentation=""):
        print(f"{indentation}Nom: {self.name}, Age: {self.age}, Infecté: {self.infected_status}, "
              f"Vaccines: {self.vaccines}, Vivante: {self.living_status}")
        for person in self.down:
            person.print_info(indentation + "  ")


def infect_a(parent, element):
    if parent.infected_status % 2 == 0 and element.infected_status % 2 != 0 and not parent.vaccines and parent.living_status:
        return 2
    return 1


def infect_b(below, element):
    if below % 3 == 0 and element.infected_status % 3 != 0 and not element.vaccines and element.living_status:
        return 3
    return 1


def infect_32_up(below, element):
    if below % 5 == 0 and element.infected_status % 5 != 0 and element.age >= 32 and not element.vaccines and element.living_status:
        return 5
    return 1


def infect_32_down(parent, element):
    if parent.infected_status % 5 == 0 and element.infected_status % 5 != 0 and element.age >= 32 and not parent.vaccines and parent.living_status:
        return 5
    return 1


def infect_ultime(below, element):
    if below % 11 == 0 and element.infected_status % 11 != 0 and (
            element.parent is None or not element.parent.living_status) and not element.vaccines and element.living_status:
        return 11
    return 1


if __name__ == "__main__":
    # Liste des valeurs pour chaque variant : Clean,1 / A,2 / B,3 / 32,5 / C,7 / Ultime,11
    # Création d'une population
    root = Person("Lola", 52, 1, True)
    nodeA = Person("Toto", 30, 1, True)
    nodeB = Person("Mary", 16, 1, True)
    nodeC = Person("Jean", 47, 1, True)
    nodeA1 = Person("Andrea", 63, 1, True)
    nodeA2 = Person("Harry", 26, 5, True)
    nodeB1 = Person("Tom", 8, 11, True)
    nodeB2 = Person("Nana", 11, 7, True)
    nodeB21 = Person("Polux", 21, 3, True)

    # Ajout de la population dans un arbre de node avec un root
    root.add_down(nodeA)
    root.add_down(nodeB)
    root.add_down(nodeC)
    nodeA.add_down(nodeA1)
    nodeA.add_down(nodeA2)
    nodeB.add_down(nodeB1)
    nodeB.add_down(nodeB2)
    nodeB1.add_down(nodeB21)

    # Lancement du spread sur la population
    root.spread_virus()
    # Application des vaccins
    root.vaccin_a1()
    root.vaccin_b1()
    root.vaccin_ultime()

    # Affichage des informations de toutes les personnes
    root.print_info()
