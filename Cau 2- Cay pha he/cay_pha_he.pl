parent('Queen Elizabeth II', 'Prince Charles').
parent('Queen Elizabeth II', 'Princess Anne').
parent('Queen Elizabeth II', 'Prince Andrew').
parent('Queen Elizabeth II', 'Prince Edward').

parent('Prince Phillip', 'Prince Charles').
parent('Prince Phillip', 'Princess Anne').
parent('Prince Phillip', 'Prince Andrew').
parent('Prince Phillip', 'Prince Edward').

parent('Prince Charles', 'Prince William').
parent('Prince Charles', 'Prince Harry').

parent('Princess Diana', 'Prince William').
parent('Princess Diana', 'Prince Harry').

parent('Princess Anne', 'Peter Phillips').
parent('Princess Anne', 'Zara Phillips').

parent('Captain Mark Phillips', 'Peter Phillips').
parent('Captain Mark Phillips', 'Zara Phillips').

parent('Prince Andrew', 'Princess Beatrice').
parent('Prince Andrew', 'Princess Eugenie').

parent('Sarah Ferguson', 'Princess Beatrice').
parent('Sarah Ferguson', 'Princess Eugenie').

parent('Sophie Rhys-jones', 'James, Viscount Severn').
parent('Sophie Rhys-jones', 'Lady Louise Mountbatten-Windsor').

parent('Prince Edward', 'James, Viscount Severn').
parent('Prince Edward', 'Lady Louise Mountbatten-Windsor').

parent('Prince William', 'Prince George').
parent('Prince William', 'Princess Charlotte').

parent('Kate Middleton', 'Prince George').
parent('Kate Middleton', 'Princess Charlotte').

parent('Autumn Kelly', 'Savannah Phillips').
parent('Autumn Kelly', 'Isla Phillips').

parent('Peter Phillips', 'Savannah Phillips').
parent('Peter Phillips', 'Isla Phillips').

parent('Zara Phillips', 'Mia Grace Tindall').

parent('Mike Tindall', 'Mia Grace Tindall').


male('Prince Phillip').
male('Prince Charles').
male('Captain Mark Phillips').
male('Timothy Laurence').
male('Prince Andrew').
male('Prince Edward').
male('Prince William').
male('Prince Harry').
male('Peter Phillips').
male('Mike Tindall').
male('James, Viscount Severn').
male('Prince George').

female('Queen Elizabeth II').
female('Princess Diana').
female('Camilla Parker Bowles').
female('Princess Anne').
female('Sarah Ferguson').
female('Sophie Rhys-jones').
female('Kate Middleton').
female('Autumn Kelly').
female('Zara Phillips').
female('Princess Beatrice').
female('Princess Eugenie').
female('Lady Louise Mountbatten-Windsor').
female('Princess Charlotte').
female('Savannah Phillips').
female('Isla Phillips').
female('Mia Grace Tindall').

married('Queen Elizabeth II', 'Prince Phillip').
married('Prince Phillip', 'Queen Elizabeth II').

married('Prince Charles', 'Camilla Parker Bowles').
married('Camilla Parker Bowles', 'Prince Charles').

married('Princess Anne', 'Timothy Laurence').
married('Timothy Laurence', 'Princess Anne').

married('Sophie Rhys-jones', 'Prince Edward').
married('Prince Edward', 'Sophie Rhys-jones').

married('Prince William', 'Kate Middleton').
married('Kate Middleton', 'Prince William').

married('Autumn Kelly', 'Peter Phillips').
married('Peter Phillips', 'Autumn Kelly').

married('Zara Phillips', 'Mike Tindall').
married('Mike Tindall', 'Zara Phillips').

divorced('Princess Diana', 'Prince Charles').
divorced('Prince Charles', 'Princess Diana').

divorced('Captain Mark Phillips', 'Princess Anne').
divorced('Princess Anne', 'Captain Mark Phillips').

divorced('Sarah Ferguson', 'Prince Andrew').
divorced('Prince Andrew', 'Sarah Ferguson').

husband(Person, Wife):- male(Person), female(Wife), married(Person, Wife).
wife(Person, Husband):- female(Person), male(Husband), married(Person, Husband).

father(Parent, Child):- male(Parent), parent(Parent, Child).
mother(Parent, Child):- female(Parent), parent(Parent, Child).

child(Child, Parent):- parent(Parent, Child).
son(Child, Parent):- male(Child), parent(Parent, Child).
daughter(Child, Parent):- female(Child), parent(Parent, Child).

grandparent(GP, GC):- parent(GP, X), parent(X, GC).
grandmother(GM, GC):- parent(GM, X), parent(X, GC), female(GM).
grandfather(GF, GC):- parent(GF, X), parent(X, GC), male(GF).
grandchild(GC, GP):- child(GC, X), child(X, GP).
grandson(GS, GP):- son(GS, X), child(X, GP).
granddaughter(GD, GP):- daughter(GD, X), child(X, GP).

sibling(Person1, Person2):- parent(X, Person1), parent(X, Person2), Person1\=Person2.
brother(Person, Sibling):- sibling(Person, Sibling), male(Person).
sister(Person, Sibling):- sibling(Person, Sibling), female(Person).

aunt(Person, NieceNephew):- sister(Person, Parent), parent(Parent, NieceNephew); brother(Uncle, Parent),wife(Person, Uncle), parent(Parent, NieceNephew).
uncle(Person, NieceNephew):- brother(Person, Parent), parent(Parent, NieceNephew); sister(Aunt, Parent), husband(Person, Aunt), parent(Parent, NieceNephew).

niece(Person, AuntUncle):-(aunt(AuntUncle, Person); uncle(AuntUncle, Person)), female(Person).
newphew(Person, AuntUncle):- (aunt(AuntUncle, Person); uncle(AuntUncle, Person)), male(Person).








