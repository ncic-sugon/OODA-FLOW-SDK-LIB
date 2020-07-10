import kfp
from kfp import compiler
import kfp.dsl as dsl
from kubernetes import client as k8s_client
from datetime import datetime
import time

# client = kfp.Client()
# EXPERIMENT_NAME = 'mlx-time-statistic-3'
# exp = client.create_experiment(name=EXPERIMENT_NAME)


class startOp(dsl.ContainerOp):
    def __init__(self):
        super(startOp, self).__init__(
            name="time-statistic-start",
            image="alpine",
            command=["sh", "-c"],
            arguments=[
                "date > /output.txt && sleep 5",
            ],
            file_outputs={
                'start': '/output.txt',
            }
        )


class cambriconOp(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, start_time):
        super(cambriconOp, self).__init__(
            name='cambricon-test',
            image='cambricon_docker_ubuntu:v1.1',
            command=['sh', '-c'],
            arguments=["cd /home/dl-plateform/mlu100-example-arm/classification/ && ./run.sh &&  date > /output.txt && echo '$0' >> /output", start_time],
            file_outputs={
                'cambricon': '/output.txt',
            }
        )


class amdOp(dsl.ContainerOp):
    def __init__(self, start_time):
        super(amdOp, self).__init__(
            name="amd",
            image='alpine',
            # image='10.18.127.1:5000/ames-housing:v1.0.0',
            command=['sh', '-c'],
            arguments=["sleep 5 && date > /output.txt && echo '$0' >> /output", start_time],
            file_outputs={
                'amd-test': '/output.txt',
            }
        )


class amd1Op(dsl.ContainerOp):
    def __init__(self, start_time):
        super(amd1Op, self).__init__(
            name="amd1",
            image='alpine',
            # image='10.18.127.1:5000/ames-housing:v1.0.0',
            command=['sh', '-c'],
            arguments=["sleep 5 && date > /output.txt && echo '$0' >> /output", start_time],
            file_outputs={
                'amd1-test': '/output.txt',
            }
        )


class armOp(dsl.ContainerOp):
    def __init__(self, start_time):
        super(armOp, self).__init__(
            name="arm",
            image='alpine:latest',
            # image='10.18.127.4:5000/arm-test:v1.0.0',
            # image='10.18.127.1:5000/ames-housing:v1.0.0',
            command=['sh', '-c'],
            arguments=["sleep 5 && date > /output.txt && echo '$0' >> /output", start_time],
            file_outputs={
                'arm-test': '/output.txt',
            }
        )


class arm1Op(dsl.ContainerOp):
    def __init__(self, start_time):
        super(arm1Op, self).__init__(
            name="arm1",
            image='alpine:latest',
            # image='10.18.127.4:5000/arm-test:v1.0.0',
            # image='10.18.127.1:5000/ames-housing:v1.0.0',
            command=['sh', '-c'],
            arguments=["sleep 5 && date > /output.txt && echo '$0' >> /output", start_time],
            file_outputs={
                'arm1-test': '/output.txt',
            }
        )


class armOp_camb(dsl.ContainerOp):
    def __init__(self, start_time):
        super(armOp_camb, self).__init__(
            name="arm_camb",
            image='alpine:latest',
            # image='10.18.127.4:5000/arm-test:v1.0.0',
            # image='10.18.127.1:5000/ames-housing:v1.0.0',
            command=['sh', '-c'],
            arguments=["sleep 5 && date > /output.txt && echo '$0' >> /output", start_time],
            file_outputs={
                'arm-camb-test': '/output.txt',
            }
        )


class endOp(dsl.ContainerOp):
    def __init__(self, output1, output2, output3):
        super(endOp, self).__init__(
            name="time-statistic-end",
            image="alpine",
            command=["sh", "-c"],
            arguments=[
                'echo "Cost Time is $0, $1, $2"', output1, output2, output3
            ],
        )


@dsl.pipeline(name='mlxpipelines', description='shows how to define dsl.Condition.')
def time_stat():
    
    start = startOp().add_node_selector_constraint('beta.kubernetes.io/arch', 'amd64').add_volume(
                k8s_client.V1Volume(name='start',
                                    host_path=k8s_client.V1HostPathVolumeSource(path="/root"))).add_volume_mount(
                k8s_client.V1VolumeMount(mount_path='/root', name='start'))

    amd = amdOp(start.output).add_node_selector_constraint('beta.kubernetes.io/arch',
                                                           'amd64').add_volume(
                k8s_client.V1Volume(name='amd1',
                                    host_path=k8s_client.V1HostPathVolumeSource(path="/root"))).add_volume_mount(
                k8s_client.V1VolumeMount(mount_path='/root', name='amd1'))

    arm = armOp(start.output).add_node_selector_constraint('beta.kubernetes.io/arch',
                                                           'arm64').add_volume(
                k8s_client.V1Volume(name='arm1',
                                    host_path=k8s_client.V1HostPathVolumeSource(path="/root"))).add_volume_mount(
                k8s_client.V1VolumeMount(mount_path='/root', name='arm1'))

    camb = cambriconOp(start.output).add_volume(
        k8s_client.V1Volume(name='cambricon-mlu',
                            host_path=k8s_client.V1HostPathVolumeSource(path="/home/dl-plateform"))).add_volume_mount(
        k8s_client.V1VolumeMount(mount_path='/home/dl-plateform', name='cambricon-mlu'))
    camb.add_resource_limit("cambricon.com/mlu", "1")
    camb.add_node_selector_constraint('beta.kubernetes.io/arch', 'arm64')


    amd1 = amd1Op(amd.output).add_node_selector_constraint('beta.kubernetes.io/arch',
                                                           'amd64').add_volume(
                k8s_client.V1Volume(name='amd2',
                                    host_path=k8s_client.V1HostPathVolumeSource(path="/root"))).add_volume_mount(
                k8s_client.V1VolumeMount(mount_path='/root', name='amd2'))
    arm1 = arm1Op(arm.output).add_node_selector_constraint('beta.kubernetes.io/arch',
                                                           'arm64').add_volume(
                k8s_client.V1Volume(name='arm2',
                                    host_path=k8s_client.V1HostPathVolumeSource(path="/root"))).add_volume_mount(
                k8s_client.V1VolumeMount(mount_path='/root', name='arm2'))
    arm_camb = armOp_camb(camb.output).add_node_selector_constraint('beta.kubernetes.io/arch',
                                                                    'arm64').add_volume(
                k8s_client.V1Volume(name='camb2',
                                    host_path=k8s_client.V1HostPathVolumeSource(path="/root"))).add_volume_mount(
                k8s_client.V1VolumeMount(mount_path='/root', name='camb2'))

    end = endOp(amd1.output, arm1.output, arm_camb.output).add_node_selector_constraint('beta.kubernetes.io/arch',
                                                                                        'amd64').add_volume(
                k8s_client.V1Volume(name='end',
                                    host_path=k8s_client.V1HostPathVolumeSource(path="/root"))).add_volume_mount(
                k8s_client.V1VolumeMount(mount_path='/root', name='end'))


compiler.Compiler().compile(time_stat, 'new-time-stat-1.tar.gz')
# run = client.run_pipeline(exp.id, 'usr', 'new-time-stat-1.tar.gz')