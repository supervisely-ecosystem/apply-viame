<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/115161827/233049075-2a0930bd-d47e-4798-a121-36b11807130e.jpg"/>

# Apply VIAME

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Models">Models</a> •
  <a href="#Acknowledgment">Acknowledgment</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](../../../../supervisely-ecosystem/apply-viame)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/apply-viame)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/apply-viame)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/apply-viame)](https://supervise.ly)

</div>

# Overview

This application is an integration of an object detection module of a VIAME, which stands for the "Visual Information Analysis for Marine Environments" framework, a software system for processing and analyzing imagery and video data.

The app contains pretrained models for underwater species detection, and works only with images project. See the list of available models <a href="#Models">here</a>

# How-To-Run

1. Run the application from Ecosystem or context menu of a project / dataset

2. Select the <a href="#Models">VIAME pipeline</a>, configure the confidence treshold and output settings

3. Click `Run` button
<img src="https://user-images.githubusercontent.com/115161827/233068890-34d9f778-8b63-4dc2-b1ac-fb998c7a0590.gif" />

## Results

Depending on the save settings you configured earlier, the project will either be updated in-place or a new cloned project with annotations will be created in your workspace

<img src="https://user-images.githubusercontent.com/115161827/233068904-c92f83e6-8158-4820-8aaa-4ebac16325b5.png" />

# Models

Here is a list of all available models

|     VIAME Pipelines       |
|----------------------------------------------|
| `detector_habcam_test_yolo_only.pipe`          |
| `detector_habcam_test_hrnet_only.pipe`         |
| `detector_habcam_test_cfrnn_only.pipe`         |
| `detector_habcam_test_multi_species_only.pipe` |
| `detector_sefsc_bw_species_v2.4m_0.5x.pipe`    |
| `detector_sefsc_bw_species_v2.4m_1.0x.pipe`    |
| `detector_sefsc_bw_species_v2.4m_2.0x.pipe`    |
| `detector_sefsc_bw_species_v2.4s_0.5x.pipe`    |
| `detector_sefsc_bw_species_v2.4s_1.0x.pipe`    |
| `detector_sefsc_bw_species_v2.4s_2.0x.pipe`    |



# Acknowledgment

This app is based on the great work `VIAME`: [github](https://github.com/VIAME/VIAME). ![GitHub Org's stars](https://img.shields.io/github/stars/VIAME/VIAME?style=social)
