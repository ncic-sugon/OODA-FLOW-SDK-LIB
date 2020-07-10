import kfp
import kfp.dsl as dsl
# import kfp.notebook  # jupter
from kubernetes import client as k8s_client

print('Start client!!!!2019-11-24')
client = kfp.Client()
# EXPERIMENT_NAME = 'liu1234'
print('start exp!!!!')


# exp = client.create_experiment(name=EXPERIMENT_NAME)


class DataCollect(dsl.ContainerOp):
    def __init__(self, data_path, data_job_id, user_name):
        super(DataCollect, self).__init__(
            name="data_collect",
            image="10.18.101.90:80/library/dataset_base:v1",
            command=["bash", "-c"],
            arguments=[
                "bash /root/classify_data.sh %s %s %s && date > /root/data.txt" % (data_path, data_job_id, user_name)],
            file_outputs={"data": "/root/data.txt"}
        )


class AIClassify(dsl.ContainerOp):
    def __init__(self, pre_input, var_job_id, user_name):
        super(AIClassify, self).__init__(
            name="ai_classify",
            image="10.18.101.90:80/library/camb_arm_execute:v5",
            command=["bash", "-c"],
            arguments=["bash /root/camb/run_camb_eg.sh /home/newnfs/%s/jobs/%s resnet && date > /root/data.txt" % (
                user_name, var_job_id), "echo %s" % pre_input],
            file_outputs={"data": "/root/data.txt"}
        )


class Data_Adjust(dsl.ContainerOp):
    def __init__(self, pre_input, data_path, data_job_id, user_name):
        super(Data_Adjust, self).__init__(
            name="data_adjust",
            image="10.18.101.90:80/library/dataset_base:v1",
            command=["bash", "-c"],
            arguments=[
                "bash /root/detection_data.sh %s %s %s && date > /root/data.txt" % (data_path, data_job_id, user_name),"echo %s" % pre_input],
            file_outputs={"data": "/root/data.txt"}
        )


class AIDetection(dsl.ContainerOp):
    def __init__(self, pre_input, var_job_id, user_name):
        super(AIDetection, self).__init__(
            name="ai_detection",
            image="10.18.101.90:80/library/camb_arm_execute:v5",
            command=["bash", "-c"],
            arguments=["bash /root/camb/run_camb_eg.sh /home/newnfs/%s/jobs/%s aircraft && date > /root/data.txt" % (
                user_name, var_job_id), "echo %s" % pre_input],
            file_outputs={"data": "/root/data.txt"}
        )


class Picture_Modify(dsl.ContainerOp):
    def __init__(self, pre_input, var_job_id, user_name,log_id):
        super(Picture_Modify, self).__init__(
            name="picture_modify",
            image="10.18.101.90:80/library/camb_arm_execute:v5",
            command=["bash", "-c"],
            arguments=["python3 /root/camb/copy_ret.py --job_id=%s --user_name=%s --log_id=%s && date > /root/data.txt" % (var_job_id, user_name,log_id), "echo %s" % pre_input],
            file_outputs={"data": "/root/data.txt"},

        )


@dsl.pipeline(
    name='ldg_pipeline_test_01',
    description='one demo test'
)
def demo():
    classify_data_path = "/root/AID"
    detection_data_path = "/root/aircraft"
    user_name = "admin"
    # 检测的
    detection_job_id = "20200514-detection"
    # 分类的job_id
    classification_job_id = "20200514-classify"
    classify_camb_id = "20200514-camb-classify"
    detection_camb_id = "20200514-camb-detection"
    picture_modify_id = "20200514-camb-picture_modify"
    device_name = "dev-cambricon"

    data_collect = DataCollect(classify_data_path, classification_job_id, user_name).add_volume(k8s_client.V1Volume(
        name='nfs-storage',
        host_path=k8s_client.V1LocalVolumeSource(path="/home/newnfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/newnfs", name='nfs-storage')).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    ai_classify = AIClassify(data_collect.output, classify_camb_id, user_name).add_volume(k8s_client.V1Volume(
        name='nfs-storage',
        host_path=k8s_client.V1LocalVolumeSource(path="/home/newnfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/newnfs", name='nfs-storage')).add_volume(k8s_client.V1Volume(
        name='aaa',
        host_path=k8s_client.V1LocalVolumeSource(path="/sys/kernel/debug"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/sys/kernel/debug", name='aaa')).add_volume(k8s_client.V1Volume(
        name='bbb',
        host_path=k8s_client.V1LocalVolumeSource(path="/tmp/.X11-unix"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/tmp/.X11-unix", name='bbb')).add_volume(k8s_client.V1Volume(
        name='ccc',
        host_path=k8s_client.V1LocalVolumeSource(path="/mnt/xfs/project/camb/v8.2_arm"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/Cambricon-Test-v8.2_arm", name='ccc')).add_volume(
        k8s_client.V1Volume(
            name='ddd',
            host_path=k8s_client.V1LocalVolumeSource(path="/mnt/xfs/project/camb/arm_v8.0/v8.0_arm/ARM64-v8.0/arm64/congcan"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/congcan", name='ddd')).add_volume(
        k8s_client.V1Volume(name=device_name, host_path=k8s_client.V1HostPathVolumeSource(
            path="/dev/cambricon_c10Dev0"))).add_volume_mount(
        k8s_client.V1VolumeMount(name=device_name, mount_path="/dev/cambricon_c10Dev0")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'arm64')
    ai_classify.add_resource_limit("cambricon.com/mlu", "1")


    data_adjust = Data_Adjust(ai_classify.output,detection_data_path,detection_job_id,user_name).add_volume(k8s_client.V1Volume(
        name='nfs-storage',
        host_path=k8s_client.V1LocalVolumeSource(path="/home/newnfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/newnfs", name='nfs-storage')).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    ai_detection = AIDetection(data_adjust.output, detection_camb_id, user_name).add_volume(k8s_client.V1Volume(
        name='nfs-storage',
        host_path=k8s_client.V1LocalVolumeSource(path="/home/newnfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/newnfs", name='nfs-storage')).add_volume(k8s_client.V1Volume(
        name='aaa',
        host_path=k8s_client.V1LocalVolumeSource(path="/sys/kernel/debug"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/sys/kernel/debug", name='aaa')).add_volume(k8s_client.V1Volume(
        name='bbb',
        host_path=k8s_client.V1LocalVolumeSource(path="/tmp/.X11-unix"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/tmp/.X11-unix", name='bbb')).add_volume(k8s_client.V1Volume(
        name='ccc',
        host_path=k8s_client.V1LocalVolumeSource(path="/home/newnfs/newldg/Cambricon-Test-v8.2_arm"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/Cambricon-Test-v8.2_arm", name='ccc')).add_volume(
        k8s_client.V1Volume(
            name='ddd',
            host_path=k8s_client.V1LocalVolumeSource(path="/home/newnfs/newldg/congcan"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/congcan", name='ddd')).add_volume(
        k8s_client.V1Volume(name=device_name, host_path=k8s_client.V1HostPathVolumeSource(
            path="/dev/cambricon_c10Dev0"))).add_volume_mount(
        k8s_client.V1VolumeMount(name=device_name, mount_path="/dev/cambricon_c10Dev0")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'arm64')
    ai_detection.add_resource_limit("cambricon.com/mlu", "1")


    picture_modify = Picture_Modify(ai_detection.output, picture_modify_id, user_name,detection_camb_id).add_volume(k8s_client.V1Volume(
        name='nfs-storage',
        host_path=k8s_client.V1LocalVolumeSource(path="/home/newnfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/newnfs", name='nfs-storage')).add_volume(k8s_client.V1Volume(
        name='aaa',
        host_path=k8s_client.V1LocalVolumeSource(path="/sys/kernel/debug"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/sys/kernel/debug", name='aaa')).add_volume(k8s_client.V1Volume(
        name='bbb',
        host_path=k8s_client.V1LocalVolumeSource(path="/tmp/.X11-unix"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/tmp/.X11-unix", name='bbb')).add_volume(k8s_client.V1Volume(
        name='ccc',
        host_path=k8s_client.V1LocalVolumeSource(path="/home/newnfs/newldg/Cambricon-Test-v8.2_arm"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/Cambricon-Test-v8.2_arm", name='ccc')).add_volume(
        k8s_client.V1Volume(
            name='ddd',
            host_path=k8s_client.V1LocalVolumeSource(path="/home/newnfs/newldg/congcan"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/congcan", name='ddd')).add_volume(
        k8s_client.V1Volume(name=device_name, host_path=k8s_client.V1HostPathVolumeSource(
            path="/dev/cambricon_c10Dev0"))).add_volume_mount(
        k8s_client.V1VolumeMount(name=device_name, mount_path="/dev/cambricon_c10Dev0")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'arm64')
    picture_modify.add_resource_limit("cambricon.com/mlu", "1")




if __name__ == '__main__':
    import kfp.compiler as compiler

    compiler.Compiler().compile(demo, "demo.tar.gz")
