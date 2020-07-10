import kfp
import kfp.dsl as dsl
import random
from kubernetes import client as k8s_client

print('Start client!!!!2019-11-24')
client = kfp.Client()
# EXPERIMENT_NAME = 'liu1234'
print('start exp!!!!')


# exp = client.create_experiment(name=EXPERIMENT_NAME)


class ReadyData(dsl.ContainerOp):
    def __init__(self, data_path, data_job_id, user_name):
        super(ReadyData, self).__init__(
            name="ready_data",
            image="10.18.101.90:80/library/dataset_base:v1",
            command=["bash", "-c"],
            arguments=[
                "bash /root/classify_data.sh %s %s %s && date > /root/data.txt" % (data_path, data_job_id, user_name)],
            file_outputs={"data": "/root/data.txt"}
        )


class CambARMExecute(dsl.ContainerOp):
    def __init__(self, pre_input, var_job_id, user_name):
        super(CambARMExecute, self).__init__(
            name="camb_execute",
            image="10.18.101.90:80/library/camb_arm_execute:v5",
            command=["bash", "-c"],
            arguments=["bash /root/camb/run_camb_eg.sh /home/newnfs/%s/jobs/%s resnet && date > /root/data.txt" % (user_name, var_job_id),"echo %s"%pre_input],
        )



@dsl.pipeline(
    name='ldg_pipeline_test_01',
    description='one demo test'
)
def demo():

    '''
    data_path = "/home/newnfs/hyperai_data/Foundation/AID", user_name = "admin",data_job_id = "20191203-1951-data",model_job_id = "20191203-1951-model",var_job_id = "20191203-1951-var",lr = 0.0010000000475,epoch = 2520,batch_size = 8

    :return:
    '''

    data_path = "/root/AID"
    user_name = "admin"
    # 分类的job_id
    classification_job_id = "20200514-classify"

    data = ReadyData(data_path, classification_job_id, user_name).add_volume(k8s_client.V1Volume(
        name='nfs-storage',
        host_path=k8s_client.V1LocalVolumeSource(path="/home/newnfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/newnfs", name='nfs-storage')).add_node_selector_constraint('beta.kubernetes.io/arch', 'amd64')


    camb = CambARMExecute(data.output, classification_job_id, user_name).add_volume(k8s_client.V1Volume(
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
        k8s_client.V1VolumeMount(mount_path="/home/Cambricon-Test-v8.2_arm", name='ccc')).add_volume(k8s_client.V1Volume(
        name='ddd',
        host_path=k8s_client.V1LocalVolumeSource(path="/mnt/xfs/project/camb/arm_v8.0/v8.0_arm/ARM64-v8.0/arm64/congcan"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/congcan", name='ddd')).add_volume(k8s_client.V1Volume(
        name='eee',
        host_path=k8s_client.V1LocalVolumeSource(path="/mnt/xfs/project/camb/v8.0/Cambricon-MLU100/datasets"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/datasets", name='eee')).add_volume(k8s_client.V1Volume(
        name='fff',
        host_path=k8s_client.V1LocalVolumeSource(path="/mnt/xfs/project/camb/v8.0/Cambricon-MLU100/models"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path="/home/models", name='fff')).add_node_selector_constraint('beta.kubernetes.io/arch', 'arm64')


    camb.add_resource_limit("cambricon.com/mlu", "1")

    # 挂载节点上的设备驱动
    device_name = "dev-cambricon"
    camb.add_volume(k8s_client.V1Volume(name=device_name, host_path=k8s_client.V1HostPathVolumeSource(
        path="/dev/cambricon_c10Dev0"))).add_volume_mount(
        k8s_client.V1VolumeMount(name=device_name, mount_path="/dev/cambricon_c10Dev0")).add_node_selector_constraint('beta.kubernetes.io/arch', 'arm64')
    # 设置安全策略
    # camb._container.set_security_context(k8s_client.V1SecurityContext(privileged=True))
if __name__ == '__main__':
    import kfp.compiler as compiler

    compiler.Compiler().compile(demo, "demo.tar.gz")

