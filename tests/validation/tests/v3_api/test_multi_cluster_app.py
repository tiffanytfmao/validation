import pytest
from .common import * # NOQA

project = {}
project_detail = {"p1_id": None, "p2_id": None, "p_client": None, "namespace": None,
                  "cluster": None, "project": None}
global_client = {"client": None, "cluster_count": False}
answer_105version = {
    "values": {
        "defaultImage": "true",
        "externalDatabase.database": "",
        "externalDatabase.host": "",
        "externalDatabase.password": "",
        "externalDatabase.port": "3306",
        "externalDatabase.user": "",
        "image.repository": "bitnami/wordpress",
        "image.tag": "4.9.4",
        "ingress.enabled": "true",
        "ingress.hosts[0].name": "xip.io",
        "mariadb.enabled": "true",
        "mariadb.image.repository": "bitnami/mariadb",
        "mariadb.image.tag": "10.1.32",
        "mariadb.mariadbDatabase": "wordpress",
        "mariadb.mariadbPassword": "",
        "mariadb.mariadbUser": "wordpress",
        "mariadb.persistence.enabled": "false",
        "mariadb.persistence.existingClaim": "",
        "mariadb.persistence.size": "8Gi",
        "mariadb.persistence.storageClass": "",
        "nodePorts.http": "",
        "nodePorts.https": "",
        "persistence.enabled": "false",
        "persistence.existingClaim": "",
        "persistence.size": "10Gi",
        "persistence.storageClass": "",
        "serviceType": "NodePort",
        "wordpressEmail": "user@example.com",
        "wordpressPassword": "",
        "wordpressUsername": "user"
    }
}

answer = {
    "values": {
        "defaultImage": "true",
        "externalDatabase.database": "",
        "externalDatabase.host": "",
        "externalDatabase.password": "",
        "externalDatabase.port": "3306",
        "externalDatabase.user": "",
        "image.repository": "bitnami/wordpress",
        "image.tag": "4.9.8-debian-9",
        "ingress.enabled": "true",
        "ingress.hosts[0].name": "xip.io",
        "mariadb.db.name": "wordpress",
        "mariadb.db.user": "wordpress",
        "mariadb.enabled": "true",
        "mariadb.image.repository": "bitnami/mariadb",
        "mariadb.image.tag": "10.1.35-debian-9",
        "mariadb.mariadbPassword": "",
        "mariadb.master.persistence.enabled": "false",
        "mariadb.master.persistence.existingClaim": "",
        "mariadb.master.persistence.size": "8Gi",
        "mariadb.master.persistence.storageClass": "",
        "nodePorts.http": "",
        "nodePorts.https": "",
        "persistence.enabled": "false",
        "persistence.size": "10Gi",
        "persistence.storageClass": "",
        "serviceType": "NodePort",
        "wordpressEmail": "user@example.com",
        "wordpressPassword": "",
        "wordpressUsername": "user"
    }
}
new_answers = {
        "values": {
            "defaultImage": "true",
            "externalDatabase.database": "",
            "externalDatabase.host": "",
            "externalDatabase.password": "",
            "externalDatabase.port": "3306",
            "externalDatabase.user": "",
            "image.repository": "bitnami/wordpress",
            "image.tag": "4.9.8-debian-9",
            "ingress.enabled": "true",
            "ingress.hosts[0].name": "xip.io",
            "mariadb.db.name": "wordpress",
            "mariadb.db.user": "wordpress",
            "mariadb.enabled": "true",
            "mariadb.image.repository": "bitnami/mariadb",
            "mariadb.image.tag": "10.1.35-debian-9",
            "mariadb.mariadbPassword": "",
            "mariadb.master.persistence.enabled": "false",
            "mariadb.master.persistence.existingClaim": "",
            "mariadb.master.persistence.size": "8Gi",
            "mariadb.master.persistence.storageClass": "",
            "nodePorts.http": "",
            "nodePorts.https": "",
            "persistence.enabled": "false",
            "persistence.size": "10Gi",
            "persistence.storageClass": "",
            "serviceType": "NodePort",
            "wordpressEmail": "test_answers@example.com",
            "wordpressPassword": "",
            "wordpressUsername": "test_adding_answers"
        }
    }
ROLES = ["project-member"]
TEMP_VER = "cattle-global-data:library-wordpress-2.1.10"


def test_multi_cluster_app_create():
    assert_if_valid_cluster_count()
    targets = []
    for projectid in project:
        targets.append({"projectId": projectid, "type": "target"})
    client = global_client["client"]
    multiclusterapp = client.create_multiClusterApp(templateVersionId=TEMP_VER,
                                                    targets=targets,
                                                    roles=ROLES,
                                                    name=random_name(),
                                                    answers=[answer])
    multiclusterapp = wait_for_mcapp_to_active(client, multiclusterapp)
    # verify if this app is available in the cluster/project
    validate_multi_cluster_app_cluster(multiclusterapp)
    delete_multi_cluster_app(multiclusterapp)


def test_multi_cluster_role_change():
    assert_if_valid_cluster_count()
    targets = []
    for projectid in project:
        targets.append({"projectId": projectid, "type": "target"})
    client = global_client["client"]
    original_role = ["project-member"]
    multiclusterapp = client.create_multiClusterApp(templateVersionId=TEMP_VER,
                                                    targets=targets,
                                                    roles=original_role,
                                                    name=random_name(),
                                                    answers=[answer])
    multiclusterapp = wait_for_mcapp_to_active(client, multiclusterapp)
    #validate_multi_cluster_app_cluster(multiclusterapp)
    new_role = ["cluster-owner"]
    multiclusterapp = client.update(multiclusterapp, roles=new_role)
    start = time.time()
    while multiclusterapp['roles'] != new_role:
        if time.time() - start > 120:
            raise AssertionError(
             "Timed out waiting")
        time.sleep(10)
        if multiclusterapp['roles'] == new_role:
            break
    assert multiclusterapp['roles'] == new_role, "role did not update"


def test_multi_cluster_answers():
    assert_if_valid_cluster_count()
    targets = []
    project_id = project_detail["p2_id"]
    targets.append({"projectId": project_id, "type": "target"})
    client = global_client["client"]
    multiclusterapp = client.create_multiClusterApp(templateVersionId=TEMP_VER,
                                                    targets=targets,
                                                    roles=ROLES,
                                                    name="tiff-answer" + random_name(),
                                                    answers=[new_answers])
    multiclusterapp = wait_for_mcapp_to_active(client, multiclusterapp)
    validate_multi_cluster_app_cluster(multiclusterapp)
    app_id = multiclusterapp.targets[0].appId
    assert app_id is not None, "app_id is None"

    project_client = \
        project[multiclusterapp.targets[0].projectId]["p_client"]
    wait_for_answers_to_be_added(project_client, app_id)


def wait_for_answers_to_be_added(client, app_id,):
    app_data = client.list_app(name=app_id).data
    if len(app_data) == 1:
        #already created
        return
    application = app_data[0]
    for k in application['answers']:
        assert application['answers'][k] == new_answers["values"][k], "answer did not match"


def test_multi_cluster_app_delete():
    assert_if_valid_cluster_count()
    targets = []
    for projectid in project:
        targets.append({"projectId": projectid, "type": "target"})
    client = global_client["client"]
    multiclusterapp = client.create_multiClusterApp(templateVersionId=TEMP_VER,
                                                    targets=targets,
                                                    roles=ROLES,
                                                    name=random_name(),
                                                    answers=[answer])
    multiclusterapp = wait_for_mcapp_to_active(client, multiclusterapp)
    validate_multi_cluster_app_cluster(multiclusterapp)
    delete_multi_cluster_app(multiclusterapp)
    for i in range(0, len(multiclusterapp.targets)):
        app_id = multiclusterapp.targets[i].appId
        assert app_id is not None, "app_id is None"
        project_client = \
            project[multiclusterapp.targets[i].projectId]["p_client"]
        wait_for_app_to_be_deleted_project(project_client, app_id)


def wait_for_app_to_be_deleted_project(client, app_id,
                           timeout=DEFAULT_MULTI_CLUSTER_APP_TIMEOUT):
    app_data = client.list_app(name=app_id).data
    start = time.time()
    if len(app_data) == 0:
        print("already done");
        return
    application = app_data[0]
    while application.state == "removing":
        if time.time() - start > timeout:
            raise AssertionError(
                "Timed out waiting for state to get to delete")
        time.sleep(.5)
        app = client.list_app(name=app_id).data
        if len(app) == 0:
            break


def test_multi_cluster_add_target():
    assert_if_valid_cluster_count()
    targets = []
    project_id = project_detail["p2_id"]
    targets.append({"projectId": project_id, "type": "target"})
    client = global_client["client"]
    multiclusterapp = client.create_multiClusterApp(templateVersionId=TEMP_VER,
                                                    targets=targets,
                                                    roles=ROLES,
                                                    name="tiff-target"+random_name(),
                                                    answers=[answer])
    multiclusterapp = wait_for_mcapp_to_active(client, multiclusterapp)
    validate_multi_cluster_app_cluster(multiclusterapp)
    app_id = multiclusterapp.targets[0].appId
    assert app_id is not None, "app_id is None"

    project_client = \
        project[multiclusterapp.targets[0].projectId]["p_client"]
    wait_for_target_to_be_added(project_client, app_id)


def wait_for_target_to_be_added(client, app_id,
                                       timeout=DEFAULT_MULTI_CLUSTER_APP_TIMEOUT):
    app_data = client.list_app(name=app_id).data
    start = time.time()
    if len(app_data) == 1:
        return
    application = app_data[0]
    while application.state != "active":
        if time.time() - start > timeout:
            raise AssertionError(
                "Timed out waiting for state to get to delete")
        time.sleep(.5)
        app = client.list_app(name=app_id).data
        if len(app) == 1:
            break;

def test_multi_cluster_delete_target():
    assert_if_valid_cluster_count()
    targets = []
    project_id = project_detail["p1_id"]
    targets.append({"projectId": project_id, "type": "target"})
    client = global_client["client"]
    multiclusterapp = client.create_multiClusterApp(templateVersionId=TEMP_VER,
                                                    targets=targets,
                                                    roles=ROLES,
                                                    name="tiff-target" + random_name(),
                                                    answers=[answer])
    multiclusterapp = wait_for_mcapp_to_active(client, multiclusterapp)
    validate_multi_cluster_app_cluster(multiclusterapp)
    app_id = multiclusterapp.targets[0].appId
    assert app_id is not None, "app_id is None"

    project_client = \
        project[multiclusterapp.targets[0].projectId]["p_client"]
    delete_multi_cluster_app(multiclusterapp)
    wait_for_app_to_be_deleted_project(project_client, app_id)


def test_multi_cluster_app_edit():
    assert_if_valid_cluster_count()
    client = global_client["client"]
    targets = []
    for projectid in project:
        targets.append({"projectId": projectid, "type": "target"})
    temp_ver = "cattle-global-data:library-wordpress-1.0.5"
    multiclusterapp = client.create_multiClusterApp(templateVersionId=temp_ver,
                                                    targets=targets,
                                                    roles=ROLES,
                                                    name=random_name(),
                                                    answers=[answer_105version]
                                                    )
    multiclusterapp = wait_for_mcapp_to_active(client, multiclusterapp)
    # verify if this app is available in the cluster/project
    validate_multi_cluster_app_cluster(multiclusterapp)
    temp_ver = "cattle-global-data:library-wordpress-2.1.10"
    multiclusterapp = client.update(multiclusterapp, uuid=multiclusterapp.uuid,
                                    templateVersionId=temp_ver,
                                    roles=ROLES,
                                    answers=[answer])
    multiclusterapp = wait_for_mcapp_to_active(client, multiclusterapp)
    # verify if this app is available in the cluster/project
    #check if correct field was changed
    validate_multi_cluster_app_cluster(multiclusterapp)
    delete_multi_cluster_app(multiclusterapp)


@pytest.fixture(scope='module', autouse="True")
def create_project_client(request):
    client, clusters = get_admin_client_and_cluster_mcapp()
    if len(clusters) > 1:
        global_client["cluster_count"] = True
    assert_if_valid_cluster_count()
    cluster1 = clusters[0]
    cluster2 = clusters[1]
    p1, ns1 = create_project_and_ns(ADMIN_TOKEN, cluster1, "target_test_1")
    p_client1 = get_project_client_for_token(p1, ADMIN_TOKEN)
    p2, ns2 = create_project_and_ns(ADMIN_TOKEN, cluster2, "target_test_2")
    p_client2 = get_project_client_for_token(p2, ADMIN_TOKEN)
    project_detail["p1_id"] = p1.id
    project_detail["namespace"] = ns1
    project_detail["p_client"] = p_client1
    project_detail["cluster"] = cluster1
    project_detail["project"] = p1
    project[p1.id] = project_detail
    project_detail["namespace"] = ns2
    project_detail["p2_id"] = p2.id
    project_detail["p_client"] = p_client2
    project_detail["cluster"] = cluster2
    project_detail["project"] = p2
    project[p2.id] = project_detail
    global_client["client"] = client

    def fin():
        client_admin = get_admin_client()
        client_admin.delete(project[p1.id]["project"])
        client_admin.delete(project[p2.id]["project"])
    request.addfinalizer(fin)


def assert_if_valid_cluster_count():
    assert global_client["cluster_count"], \
        "Setup Failure. Tests require atleast 2 clusters"


def validate_multi_cluster_app_cluster(multiclusterapp):
    for i in range(1, len(multiclusterapp.targets)):
        app_id = multiclusterapp.targets[i].appId
        assert app_id is not None, "app_id is None"
        project_client = \
            project[multiclusterapp.targets[i].projectId]["p_client"]
        wait_for_app_to_active(project_client, app_id)
        validate_app_version(project_client, multiclusterapp, app_id)
        validate_response_app_endpoint(project_client, app_id)


def get_admin_client_and_cluster_mcapp():
    clusters = []
    client = get_admin_client()
    if CLUSTER_NAME != "" and CLUSTER_NAME_2 != "":
        assert len(client.list_cluster(name=CLUSTER_NAME).data) != 0,\
            "Cluster is not available: %r" % CLUSTER_NAME
        assert len(client.list_cluster(name=CLUSTER_NAME_2).data) != 0,\
            "Cluster is not available: %r" % CLUSTER_NAME_2
        clusters.append(client.list_cluster(name=CLUSTER_NAME).data[0])
        clusters.append(client.list_cluster(name=CLUSTER_NAME_2).data[0])
    else:
        clusters = client.list_cluster().data
    return client, clusters


def delete_multi_cluster_app(multiclusterapp):
    client = global_client["client"]
    uuid = multiclusterapp.uuid
    name = multiclusterapp.name
    client.delete(multiclusterapp)
    mcapps = client.list_multiClusterApp(uuid=uuid, name=name).data
    assert len(mcapps) == 0, "Multi Cluster App is not deleted"


def validate_app_version(project_client, multiclusterapp, app_id):
    temp_version = multiclusterapp.templateVersionId
    app = temp_version.split(":")[1].split("-")
    mcapp_template_version = "catalog://?catalog=" + app[0] + \
                             "&template=" + app[1] + "&version=" + app[2]
    app_template_version = \
        project_client.list_app(name=app_id).data[0].externalId
    assert mcapp_template_version == app_template_version, \
        "App Id is different from the Multi cluster app id"
