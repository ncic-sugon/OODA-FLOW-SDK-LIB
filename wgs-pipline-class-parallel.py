# wgs-pipline-class2.py
# 导入相关pipeline包
import kfp
from kfp import compiler
import kfp.dsl as dsl
import kfp.gcp as gcp
from kubernetes import client as k8s_client

client = kfp.Client()
print('start client')


# 开始节点
class wgsstart(dsl.ContainerOp):
    """validation for file"""

    def __init__(self):
        super(wgsstart, self).__init__(
            name='time-start',
            image='10.18.101.90:80/library/wgs-start-end:latest',
            command=['./root/app/start.sh'],
            file_outputs={
                'start': '/output.txt',
            })


# 开始基因测序，以下直至end结束，定义相关类对象
class wgssplit(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgssplit, self).__init__(
            name='wgs-split-first',
            image='10.18.101.90:80/library/wgs-split:latest',
            command=['./root/app/split.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'split': '/output.txt',
            })


class wgsbwa(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgsbwa, self).__init__(
            name='wgs-bwa-1',
            image='10.18.101.90:80/library/wgs-bwa:latest',
            command=['./root/app/wgs_bwa.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'bwa': '/output.txt',
            })


class wgsbwa1(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgsbwa1, self).__init__(
            name='wgs-bwa-2',
            image='10.18.101.90:80/library/wgs-bwa:latest',
            command=['./root/app/wgs_bwa1.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'bwa': '/output.txt',
            })


class wgssam(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgssam, self).__init__(
            name='wgs-samtools-1',
            image='10.18.101.90:80/library/wgs-samtools:latest',
            command=['./root/app/wgs_samtools.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'sam': '/output.txt',
            })


class wgssam1(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgssam1, self).__init__(
            name='wgs-samtools-2',
            image='10.18.101.90:80/library/wgs-samtools:latest',
            command=['./root/app/wgs_samtools1.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'sam1': '/output.txt',
            })


class wgsmer(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None, validate1=None):
        super(wgsmer, self).__init__(
            name='wgs-merge-first',
            image='10.18.101.90:80/library/wgs-merge:latest',
            command=['./root/app/merge.sh'],
            arguments=[
                '--validate', validate,
                '--validate1', validate1,
            ],
            file_outputs={
                'mer': '/output.txt',
            })


class wgssplit1(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgssplit1, self).__init__(
            name='wgs-split-second',
            image='10.18.101.90:80/library/wgs-split-bam:latest',
            command=['./root/app/split.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'split': '/output.txt',
            })


### step-3 PICARD
class wgspic(dsl.ContainerOp):
    def __init__(self, validate=None):
        super(wgspic, self).__init__(
            name='wgs-picard-1',
            image='10.18.101.90:80/library/wgs-picard:latest',
            command=['./root/app/wgs_picard1.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'pic': '/output.txt',
            })


### step-3 PICARD
class wgspic1(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgspic1, self).__init__(
            name='wgs-picard-2',
            image='10.18.101.90:80/library/wgs-picard:latest',
            command=['./root/app/wgs_picard2.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'pic': '/output.txt',
            })


### step-4 InDel
class wgsind(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgsind, self).__init__(
            name='wgs-indel-1',
            image='10.18.101.90:80/library/wgs-indel:latest',
            command=['./root/app/wgs_indel1.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'ind': '/output.txt',
            })


class wgsind1(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgsind1, self).__init__(
            name='wgs-indel-2',
            image='10.18.101.90:80/library/wgs-indel:latest',
            command=['./root/app/wgs_indel2.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'ind': '/output.txt',
            })


### step-5 BQSR
class wgsbqs(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgsbqs, self).__init__(
            name='wgs-bqsr-1',
            image='10.18.101.90:80/library/wgs-bqsr:latest',
            command=['./root/app/wgs_bqsr1.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'bqs': '/output.txt',
            })


### step-5 BQSR
class wgsbqs1(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgsbqs1, self).__init__(
            name='wgs-bqsr1-2',
            image='10.18.101.90:80/library/wgs-bqsr:latest',
            command=['./root/app/wgs_bqsr2.sh'],
            arguments=[
                '--validate', validate,
            ],
            file_outputs={
                'bqs': '/output.txt',
            })


### step-6 call
class wgscal(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgscal, self).__init__(
            name='wgs-call-1',
            image='10.18.101.90:80/library/wgs-call:latest',
            command=['./root/app/wgs_call1.sh'],
            arguments=['--validate', validate],
            file_outputs={
                'cal': '/output.txt',
            })


class wgscal1(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None):
        super(wgscal1, self).__init__(
            name='wgs-call-2',
            image='10.18.101.90:80/library/wgs-call:latest',
            command=['./root/app/wgs_call2.sh'],
            arguments=['--validate', validate],
            file_outputs={
                'cal': '/output.txt',
            })


# 基因测序结束标志
class wgsend(dsl.ContainerOp):
    """test images-wgs-nfs:v1"""

    def __init__(self, validate=None, validate1=None):
        super(wgsend, self).__init__(
            name='time-end',
            image='10.18.101.90:80/library/wgs-start-end:latest',
            command=['./root/app/end.sh'],
            arguments=['--validate', validate,
                       '--validate1', validate1,
                       ],
            file_outputs={
                'end': '/output.txt',
            })


@dsl.pipeline(
    name='hello_wgs_demo11',
    description='bwa samtools pcard and gatk')
def wgs_demo():
    # 实例化对象，并挂载存储节点，并指定计算节点，该节点运行于AMD64
    start = wgsstart().add_volume(k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
        path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')
    # 实例化对象，挂载储存节点，指定计算节点，开始测序
    split = wgssplit(start.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')
    # 实例化对象，挂载储存节点，指定计算节点
    bwa = wgsbwa(split.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    bwa1 = wgsbwa1(split.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    sam = wgssam(bwa.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    sam1 = wgssam1(bwa1.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    mer = wgsmer(sam.output, sam1.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    sp1 = wgssplit1(mer.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    pic = wgspic(sp1.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    pic1 = wgspic1(sp1.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    ind = wgsind(pic.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')
    # 实例化对象，挂载储存节点，指定计算节点
    ind1 = wgsind1(pic1.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    bqs = wgsbqs(ind.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    bqs1 = wgsbqs1(ind1.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    cal = wgscal(bqs.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点
    cal1 = wgscal1(bqs1.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')

    # 实例化对象，挂载储存节点，指定计算节点，结束标志
    end = wgsend(cal.output, cal1.output).add_volume(
        k8s_client.V1Volume(name='wgs-data', host_path=k8s_client.V1HostPathVolumeSource(
            path="/mnt/xfs"))).add_volume_mount(
        k8s_client.V1VolumeMount(name='wgs-data', mount_path="/mnt/xfs")).add_node_selector_constraint(
        'beta.kubernetes.io/arch', 'amd64')


if __name__ == '__main__':
    # 生成pipeline的yaml压缩包文件
    import kfp.compiler as compiler

    compiler.Compiler().compile(wgs_demo, 'all_wgs.tar.gz')
    print("Complate.")