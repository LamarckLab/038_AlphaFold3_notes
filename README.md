## Lamarck &nbsp; &nbsp; &nbsp; 2026-03-25
#### 该文档使用Docker部署AlphaFold3
---

## 01  基础镜像的准备
> 官方文档的 Dockerfile 里提到，alphafold3 会把 cuda-12.6.3-base-ubuntu24.04 作为基础镜像；
> Linux服务器很容易连不上Docker hub，无法正常执行docker pull，所以先在 windows 上拿到这个基础镜像
>
在 windows 的 cmd 中执行以下命令，可以通过执行 docker images 检查
```bash
docker pull nvidia/cuda:12.6.3-base-ubuntu22.04
```
打包该基础镜像，会输出到工作目录中
```bash
docker save -o cuda12.6.3.tar nvidia/cuda:12.6.3-base-ubuntu22.04
```
把该打包文件上传到 linux 服务器之后，将其导入到服务器的 Docker 本地镜像仓库中
```bash
docker load -i cuda12.6.3.tar
```

## 02  克隆官方的源码仓库
> **236机子路径 /data/lmk/alphafold3**
```bash
git clone https://github.com/google-deepmind/alphafold3.git
```

## 03  准备MSA所需的数据库
> **236机子路径 /data/lmk/alphafold3_databases**  
> **pdb_2022_09_28_mmcif_files.tar 需要解压成 mmcif_files,共十个文件，总计627GB**
```bash
├── bfd-first_non_consensus_sequences.fasta -17G
├── mgy_clusters_2022_05.fa -120G
├── mmcif_files -4.1M
├── nt_rna_2023_02_23_clust_seq_id_90_cov_80_rep_seq.fasta -76G
├── pdb_2022_09_28_mmcif_files.tar -234G
├── pdb_seqres_2022_09_28.fasta -223M
├── rfam_14_9_clust_seq_id_90_cov_80_rep_seq.fasta -218M
├── rnacentral_active_seq_id_90_cov_80_linclust.fasta -13G
├── uniprot_all_2021_04.fa -102G
└── uniref90_2022_05.fa -67G
```
<img src="images/pic1.jpg" alt="pic1" width="800">

## 04  准备模型权重参数
> **236机子路径 /data/lmk/alphafold3_parameters**
> *af3.bin.zst 需要解压成af3.bin*
```bash
├── af3.bin -1.1G
└── af3.bin.zst -974M
```
<img src="images/pic2.jpg" alt="pic1" width="800">

## 05  正式构建 alphafold3 镜像
Dockerfile 里默认的 timeout 时间是30s，这里提前修改成1800s了，以防中途因为网络问题而终止
> 在Dockerfile中这个位置添加了UV_HTTP_TIMEOUT=1800
<img src="images/pic3.jpg" alt="pic1" width="800">

```bash
cd /data/lmk/alphafold3
docker build -t alphafold3 -f docker/Dockerfile .
```

##### [AlphaFold3官方文档](https://github.com/google-deepmind/alphafold3)














