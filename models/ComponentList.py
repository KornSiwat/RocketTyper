class ComponentList():
    ''' class for component_list which is responsible for containing, drawing, and updating the components of the gameplay screen. '''

    def __init__(self):
        ''' create attribute of component_list instance '''

        self._components = []

    def draw(self):
        ''' call draw method of each elements in components attribute if it is not empty '''

        if len(self._components) > 0:
            [component.draw() for component in self._components]

    def add_component(self, component):
        ''' append the component parameter to the list binding to component attribute'''

        self._components.append(component)

    def update(self):
        ''' call update method of rach elements in components attribute if it isv not empty '''

        if len(self._components) > 0:
            [component.update() for component in self._components]
            [component.update_animation() for component in self._components]
