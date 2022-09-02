"""
Quentin Masingarbe, mars 2021 pour 3is

Scripts maya pour exporter les shaders depuis la scene de shading d'un asset et les reimporter sur les alembics animes
de l'asset dans la scene de rendu
"""
import maya.cmds as cmds
import json
import os


def exportShader():
    """ A executer dans la scene de shading d'un asset pour en exporter les shaders et leurs connections """
    # proposer une fenetre pour savoir ou on va exporter le shader
    dossier = cmds.fileDialog2(fileMode=3)[0]
    print("On a choisi le dossier '{}' pour exporter le shader".format(dossier))

    # choisi le nom de l'asset qu'on exporte
    result = cmds.promptDialog(
        title='Asset name',
        message="Nom de l'asset :                                              ",
        button=['OK'], defaultButton='OK'
    )
    asset_name = cmds.promptDialog(query=True, text=True)
    print("Nom de l'asset : '{}'".format(asset_name))

    # lister les geos dans la scene
    cmds.select(hi = True)
    geos = cmds.ls(selection = True, geometry = True)
    print(geos)

    # lister les shaders sur les geos
    shading_groups_to_export = list()
    print("list ok")
    for geo in geos:
        shading_groups_to_export.extend(cmds.listSets(object=geo, extendToShape=True))

    # filtre les sets qui sont renderable (set de connexion entre shading groups et geo)
    shading_groups_to_export = [s for s in shading_groups_to_export if cmds.sets(s, query=True, renderable=True)]
    shading_groups_to_export = list(set(shading_groups_to_export))
    print("On a trouve {} shading groups a exporter".format(len(shading_groups_to_export)))

    # exporter les shaders dans un .ma
    cmds.select(shading_groups_to_export, replace=True, noExpand=True)
    path = os.path.join(dossier + r"\{}_shaders.ma".format(asset_name))
    cmds.file(path, typ="mayaAscii", exportSelected=True)
    print("On a export les shaders ici : '{}'".format(path))

    # stocker quel shader va sur quelle geo
    correspondence = dict()
    for shading_group in shading_groups_to_export:
        objects = cmds.sets(shading_group, query=True)
        correspondence[shading_group] = objects

    # exporter l'information dans un json
    path = os.path.join(dossier, "{}_correspondence.json".format(asset_name))
    with open(path, 'w') as f:
        json.dump(correspondence, f)
    print("On a export la correspondence ici : '{}'".format(path))

    print("Success !")


def relinkShader():
    """
    A executer dans la scene de rendu, essaie de relinker les shaders pour chaque namespace qui correpsond a un asset
    Exemple pour les geos avec namespace bob_01, on essaie d'applique le shading de l'objet bob
    """
    # proposer une fenetre pour savoir ou son exporte les shadings
    dossier = cmds.fileDialog2(fileMode=3)[0]
    fichiers = os.listdir(dossier)
    print("On va chercher les shaders dans ce dossier : '{}'".format(dossier))

    # lister les namespaces dans la scene
    namespaces = cmds.namespaceInfo(":", listOnlyNamespaces=True)
    namespaces = [n for n in namespaces if n not in ["UI", "shared"]]

    # pour chaque namespace
    for namespace in namespaces:
        # checker si il coorrespond au nom d'un asset
        if "_" not in namespace:
            continue
        if namespace.startswith("shader_"):  # bypass les ma de shaders deja importes
            continue
        asset_name = namespace.split("_")[0]
        print("On travaille sur l'asset '{}' avec le namespace '{}'".format(asset_name, namespace))

        # verifier que le shader a ete exporte pour cet asset
        if "{}_shaders.ma".format(asset_name) not in fichiers:
            print("On a trouve l'asset '{}' mais ses shaders ne sont pas dispo dans le dossier '{}'".format(asset_name, dossier))
            continue

        # importer les shader si ils n'existent pas encore
        shader_namespace = "shader_{}".format(asset_name)
        if shader_namespace not in cmds.namespaceInfo(":", listOnlyNamespaces=True):
            print("On importe le shader de '{}' avec le namespace '{}'".format(asset_name, shader_namespace))
            cmds.file(dossier + r"\{}_shaders.ma".format(asset_name), r=True, typ="mayaAscii", namespace="shader_{}".format(asset_name), options="v=0;")
        else:
            print("Le shader de '{}' existe deja, on ne le reimporte pas".format(asset_name))

        # recup les datas de la correspondence shader <=> geos pour cet asset
        with open(os.path.join(dossier, '{}_correspondence.json'.format(asset_name)), 'r') as f:
            correspondence = json.load(f)

        # pour chaque shader
        for shading_group_name, geos_names in correspondence.items():
            # construit le nom du shading group dans notre scene
            shading_group = "{}:{}".format(shader_namespace, shading_group_name)

            # pour chaque geo qui etait connecte au shader
            for geo_name in geos_names:
                if "[" in geo_name:  # quand c'est une selection de face
                    geo_name_namespaced = "{}:{}".format(namespace, geo_name.split(".")[0].split(":")[-1])
                    if not cmds.objExists(geo_name_namespaced):
                        print("WARNING : La correspondence indique que la geo '{}' doit avoir le shader '{}' mais on ne trouve pas cette geo dans la scene".format(geo_name_namespaced, shading_group))
                        continue
                    transforms_to_be_linked = "{}.{}".format(geo_name_namespaced, geo_name.split(".")[-1])
                else:  # quand c'est une simple shape
                    geo_name_namespaced = "{}:{}".format(namespace, geo_name.split(":")[-1])
                    geo_to_be_linked = cmds.ls([geo_name_namespaced, "{}Deformed".format(geo_name_namespaced)])  # support shapeDeformed
                    if not geo_to_be_linked:
                        print("WARNING : La correspondence indique que la geo '{}' doit avoir le shader '{}' mais on ne trouve pas cette geo dans la scene".format(geo_name_namespaced, shading_group))
                        continue
                    transforms_to_be_linked = [cmds.listRelatives(s, parent=True)[0] for s in geo_to_be_linked]

                print("On relink le shader '{}' sur la geo '{}'".format(shading_group, transforms_to_be_linked))
                cmds.sets(transforms_to_be_linked, e=True, forceElement=shading_group)

    print("Success !")
