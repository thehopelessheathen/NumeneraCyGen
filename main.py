import random
import textwrap

class CypherType:
    def __init__(self, n, d, b, f, v, t, e):
        self.name = n
        self.levelDie = int(d)
        self.levelBonus = int(b)
        self.formsList = f
        self.variantList = v
        self.thresholdList = t
        self.effectBase = e

    def printOut(self):
        return self.name + " (" + str(1 + self.levelBonus) + " - " + str(self.levelDie + self.levelBonus) + ") \nForms: " + str(self.formsList) + \
               "\n" + str(self.variantList) + "\n" + textwrap.fill("Effect: "+self.effectBase, 60)


class ArtifactType:
    def __init__(self, n, d, b, f, v, t, e, xt, xd):
        self.name = n
        self.levelDie = int(d)
        self.levelBonus = int(b)
        self.formsList = f
        self.variantList = v
        self.thresholdList = t
        self.effectBase = e
        self.depletionThreshold = int(xt)
        self.depletionDie = int(xd)

    def printOut(self):
        return self.name + " (" + str(1 + self.levelBonus) + " - " + str(self.levelDie + self.levelBonus) + ") \nForms: " + str(self.formsList) + \
               "\n" + str(self.variantList) + "\n" + textwrap.fill("Effect: "+self.effectBase, 60) + "\n" + "Depletion: "+str(self.depletionThreshold)+" in 1d"+str(self.depletionDie)


class Cypher:
    def __init__(self, template):
        self.name = template.name
        if template.levelDie > 0:
            self.level = random.randint(1, template.levelDie) + template.levelBonus
        else:
            self.level = template.levelBonus
        self.form = template.formsList[random.randint(0, len(template.formsList)-1)]
        self.variant = template.variantList[random.randint(0, len(template.variantList) - 1)]
        self.thresholdValue = "NULL"
        for thresher in template.thresholdList:
            if ':' in thresher and int(thresher[thresher.index(':') + 1:]) <= self.level:
                self.thresholdValue = thresher[:thresher.index(':')]
        self.effect = template.effectBase.replace("@", str(self.variant))
        self.effect = self.effect.replace("^", str(self.thresholdValue))
        self.effect = self.effect.replace("$", str(self.level))

    def printOut(self):
        return self.name + " (" + str(self.level) + ") \nForm: " + self.form + \
               "\n" + textwrap.fill("Effect: "+self.effect, 60)

    def textOut(self):
        return self.name + " (" + str(self.level) + ") \nForm: " + self.form + \
               "\n" + "Effect: "+self.effect

class Artifact:
    def __init__(self, template, quirk):
        self.name = template.name
        if template.levelDie > 0:
            self.level = random.randint(1, template.levelDie) + template.levelBonus
        else:
            self.level = template.levelBonus
        self.form = template.formsList[random.randint(0, len(template.formsList) - 1)]
        self.variant = template.variantList[random.randint(0, len(template.variantList) - 1)]
        self.thresholdValue = "NULL"
        for thresher in template.thresholdList:
            if ':' in thresher and int(thresher[thresher.index(':') + 1:]) <= self.level:
                self.thresholdValue = thresher[:thresher.index(':')]
        self.effect = template.effectBase.replace("@", str(self.variant))
        self.effect = self.effect.replace("^", str(self.thresholdValue))
        self.effect = self.effect.replace("$", str(self.level))
        if template.depletionDie <= 0:
            self.depletion = "Automatic"
        elif template.depletionThreshold <= 0:
            self.depletion = "—"
        elif template.depletionThreshold == 1:
            self.depletion = "1 in 1d"+str(template.depletionDie)
        else:
            self.depletion = "1-" + str(template.depletionThreshold) + " in 1d" + str(template.depletionDie)
        self.quirk = quirk

    def printOut(self):
        return self.name + " (" + str(self.level) + ") \nForm: " + self.form + \
            "\n" + textwrap.fill("Effect: " + self.effect, 60) + "\n" + textwrap.fill("Quirk: " + self.quirk, 60) + "\nDepletion: " + self.depletion

    def textOut(self):
        return self.name + " (" + str(self.level) + ") \nForm: " + self.form + \
            "\n" + "Effect: " + self.effect + "\n" + "Quirk: " + self.quirk + "\nDepletion: " + self.depletion


def getItemTypes(fulltext, isartifact):
    typelist = []
    while '{' in fulltext:
        subtext = fulltext[fulltext.index('{') + 1:]
        name = subtext[:subtext.index('\n')]
        subtext = subtext[subtext.index(';') + 1:]

        if subtext[:subtext.index('\n')].strip() != "":
            levelDie = subtext[:subtext.index('\n')]
        else:
            levelDie = 0
        subtext = subtext[subtext.index(';') + 1:]

        if subtext[:subtext.index('\n')].strip() != "":
            levelBonus = subtext[:subtext.index('\n')]
        else:
            levelBonus = 0
        subtext = subtext[subtext.index(';') + 1:]

        if subtext[:subtext.index('\n')].strip() != "":
            forms = subtext[:subtext.index('\n')].split(', ')
        else:
            forms = ["NULL"]
        subtext = subtext[subtext.index(';') + 1:]

        if subtext[:subtext.index('\n')].strip() != "":
            variantWeights = subtext[:subtext.index('\n')].split(', ')
            variantList = []
            for v in variantWeights:
                weight = int(v[v.index(':') + 1:])
                variant = v[:v.index(':')]
                for count in range(weight):
                    variantList.append(variant)
        else:
            variantList = ["NULL"]
        subtext = subtext[subtext.index(';') + 1:]

        if subtext[:subtext.index('\n')].strip() != "":
            thresholdList = subtext[:subtext.index('\n')].split(', ')
        else:
            thresholdList = ["NULL"]
        subtext = subtext[subtext.index(';') + 1:]

        if isartifact:
            if subtext[:subtext.index('\n')].strip() != "":
                depletionThreshold = subtext[:subtext.index('\n')]
            else:
                depletionThreshold = 0
            subtext = subtext[subtext.index(';') + 1:]

            if subtext[:subtext.index('\n')].strip() != "":
                depletionDie = subtext[:subtext.index('\n')]
            else:
                depletionDie = 0
            subtext = subtext[subtext.index(';') + 1:]

        if subtext[:subtext.index('\n')].strip() != "":
            effect = subtext[:subtext.index('}') - 1]
        else:
            effect = "NULL"

        if isartifact:
            cy = ArtifactType(name, levelDie, levelBonus, forms, variantList, thresholdList, effect, depletionThreshold, depletionDie)
        else:
            cy = CypherType(name, levelDie, levelBonus, forms, variantList, thresholdList, effect)
        typelist.append(cy)
        fulltext = fulltext[fulltext.index('}')+1:]
    return typelist


def getQuirks(fulltext):
    quirkList = fulltext.split("\n")
    return quirkList


def checkDupe(lister, subject):
    if len(lister) == 0:
        return False
    for iterator in lister:
        if subject.form == iterator.form and subject.name == iterator.name:
            return True
    return False


def createCypherBatch(cypherLibrary, quantity, antiDupe):
    print("Generating cypher batch...\n")
    batchfile = None
    mark = 1
    while batchfile is None:
        try:
            batchfile = open("D:\\Programming\\Cypher Batches\\Cypher Batch " + str(mark) + ".txt", 'x')
        except FileExistsError:
            mark += 1
    print("Populating batch...\n")
    cypherList = []
    for x in range(quantity):
        if antiDupe == "y":
            cypher = Cypher(cypherLibrary[random.randint(0, (len(cypherLibrary) - 1))])
            while checkDupe(cypherList, cypher):
                cypher = Cypher(cypherLibrary[random.randint(0, (len(cypherLibrary) - 1))])
        else:
            cypher = Cypher(cypherLibrary[random.randint(0, (len(cypherLibrary) - 1))])
        cypherList.append(cypher)
        batchfile.write(cypher.textOut() + "\n\n")
    print("Done! You can find your cyphers at " + "D:\\Programming\\Cypher Batches\\Cypher Batch " + str(mark) + ".txt")


def createArtifactBatch(artifactLibrary, quantity, antiDupe, quirklist):
    print("Generating artifact batch...\n")
    batchfile = None
    mark = 1
    while batchfile is None:
        try:
            batchfile = open("D:\\Programming\\Cypher Batches\\Artifact Batch " + str(mark) + ".txt", 'x')
        except FileExistsError:
            mark += 1
    print("Populating batch...\n")

    artifactList = []
    quirkWeightList = []
    for q in quirklist:
        quirk = q[q.index(':') + 1:]
        weight = int(q[:q.index(':')])
        for count in range(weight):
            quirkWeightList.append(quirk)

    for x in range(quantity):
        quirk = quirkWeightList[random.randint(0, (len(quirkWeightList) - 1))]
        if antiDupe == "y":
            artifact = Artifact(artifactLibrary[random.randint(0, (len(artifactLibrary) - 1))], quirk)
            while checkDupe(artifactList, artifact):
                artifact = Artifact(artifactLibrary[random.randint(0, (len(artifactLibrary) - 1))], quirk)
        else:
            artifact = Artifact(artifactLibrary[random.randint(0, (len(artifactLibrary) - 1))], quirk)
        artifactList.append(artifact)
        batchfile.write(artifact.textOut() + "\n\n")
    print("Done! You can find your artifacts at " + "D:\\Programming\\Cypher Batches\\Artifact Batch " + str(
        mark) + ".txt")


library = []
itemType = input("Would you like to generate cyphers (enter c) or artifacts (enter a)?")
itemNum = int(input("How many would you like to create?"))
duplicates = input("Would you like to prevent duplicates? (enter y for yes or n for no)")
if itemType == "a":
    file = open('Discovery Artifact Catalog')
    library.extend(getItemTypes(file.read(), True))
    file = open('Custom Artifact Catalog')
    library.extend(getItemTypes(file.read(), True))
    file = open('Quirk Catalog')
    quirklist = getQuirks(file.read())
    createArtifactBatch(library, itemNum, duplicates, quirklist)
else:
    file = open('Discovery Catalog')
    library.extend(getItemTypes(file.read(), False))
    file = open('Destiny Catalog')
    library.extend(getItemTypes(file.read(), False))
    file = open('Custom Catalog')
    library.extend(getItemTypes(file.read(), False))
    createCypherBatch(library, itemNum, duplicates)
