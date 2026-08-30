<p align="left">
  <a href="./README_EN.md">Homepage</a>
</p>
<p align="right">
  <strong>English</strong> | <a href="../AlphaFold3_Setup.md">中文</a>
</p>

## Lamarck &nbsp; &nbsp; &nbsp; 2026-03-25
#### This document deploys AlphaFold3 with Docker
---

## 01  Preparing the base image
> The official Dockerfile notes that alphafold3 builds on cuda-12.6.3-base-ubuntu22.04 as its base image;
> a Linux server often cannot reach Docker Hub and `docker pull` fails there, so pull the base image on Windows first
>
Run the following in the Windows cmd, then check with `docker images`
```bash
docker pull nvidia/cuda:12.6.3-base-ubuntu22.04
```
Export the base image; the archive lands in the working directory
```bash
docker save -o cuda12.6.3.tar nvidia/cuda:12.6.3-base-ubuntu22.04
```
Upload the archive to the Linux server, then load it into the server's local Docker image store
```bash
docker load -i cuda12.6.3.tar
```

## 02  Cloning the official source repository
> **Path on the 236 machine: /data/lmk/alphafold3**
```bash
git clone https://github.com/google-deepmind/alphafold3.git
```

## 03  Preparing the MSA databases
> **Path on the 236 machine: /data/lmk/alphafold3_databases**  
> **pdb_2022_09_28_mmcif_files.tar has to be extracted into mmcif_files — ten files in total, 627 GB**
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
<img src="../images/pic1.jpg" alt="pic1" width="800">

## 04  Preparing the model weights
> **Path on the 236 machine: /data/lmk/alphafold3_parameters**
> *af3.bin.zst has to be decompressed into af3.bin*
```bash
├── af3.bin -1.1G
└── af3.bin.zst -974M
```
<img src="../images/pic2.jpg" alt="pic1" width="800">

## 05  Building the alphafold3 image
The Dockerfile's default timeout is 30s; it was raised to 1800s up front so a network hiccup does not abort the build
> `UV_HTTP_TIMEOUT=1800` was added at this spot in the Dockerfile
<img src="../images/pic3.jpg" alt="pic1" width="800">

```bash
cd /data/lmk/alphafold3
docker build -t alphafold3 -f docker/Dockerfile .
```

##### [AlphaFold3 official documentation](https://github.com/google-deepmind/alphafold3)
