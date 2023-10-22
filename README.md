# Capstone-2023-1-01



## 1. 프로젝트 소개
### 1.1 연구배경
현대 의학에서 질병의 진단 및 치료를 위해 사용되는 영상으로 CT, MR, 초음파 영상 등이 주로 사용되고 있다. 컴퓨터단층촬영(CT), 자기공명촬영(MRI) 장치 등과 같은 의료기기를 통해 얻어진 인체내부의 단면 사진을 이용한 특정 장기의 분리, 종양 검출 및 3D 재구성 등과 같은 의료영상 처리기술은 치료나 수술을 위한 계획이나 방법 등을 결정하는데 매우 중요한 역할을 한다. 현재의 진단은 의료인들의 전문적인 지식과 경험에 의해 시각적으로 이루어지고 있지만, 컴퓨터를 이용하여 진단을 한다면 진단 시간을 단축하고 진단의 정확성 및 많은 양의 영상 데이터를 처리할 수 있다.

### 1.2 기존문제점
복부 CT를 이용한 장기 Segmentation과 관련된 논문은 흔히 찾아볼 수 있었다. 그러나 특정 장기나 특정 질병에 집중하고 있고, 이를 직접적으로 시각화 하는 프로그램에 관한 논문을 찾기 어려웠다. 기존의 시각화 프로그램인 3D Slicer의 경우 많은 기능을 가지고 있지만 프로그램을 이용하기에 무거운 측면이 있고, 별도의 전문적인 지식이 요구된다.

### 1.3 목표
많은 Segmentation관련 연구가 활발히 진행되는 가운데, 우리는 Segmentation된 이미지를 실제 환경에서 보다 사용하기 용이하도록 시각화 프로그램을 제작하고자 한다.

## 2. 팀 소개
이주승 juicy0123@naver.com (학습모델개발 및 최적화, 학습모델 테스트, 데이터전처리)

전도현 fkl9874@pusan.ac.kr (학습모델개발 및 최적화,예측결과도출,데이터전처리 모듈수정)

김병관, qud654@pusan.ac.kr (데이터전처리, 학습모델 테스트, 학습모델 최적화 및 오류수정)

## 3. 시스템 구성도
![Pipeline](https://github.com/pnucse-capstone/capstone-2023-1-01/assets/48307605/697c539d-02cb-4c4c-b7d8-97ac4296853e)

### 3.1 데이터 수집
![Grand_challenge](https://github.com/pnucse-capstone/capstone-2023-1-01/assets/48307605/e13e59a1-6dd6-40e4-8819-ae7b28266505)
 본 과제에서 다룰 데이터는 논문 “AbdomenCT-1K: Is Abdominal Organ Segmentation A Solved Problem?” 의 공식 데이터셋을 사용하였다. 해당 논문에서는 기존에 있던 논문들의 단일 장기 데이터셋에서 간, 신장, 비장, 췌장의 복부CT 장기segmentation 데이터셋을 수집하였고 현재 활발히 연구되고 있는 주제인 fully supervised learning, semi-supervised learning, weakly supervised learning, continual learning에 대한 benchmark를 만들어 두었다. 우리는 fully supervised learning의 데이터셋과 성능 측정 지표를 사용하였다.

### 3.2 데이터 전처리 및 학습
![kubernetes](https://github.com/pnucse-capstone/capstone-2023-1-01/assets/48307605/3491eb0f-fe70-4bd8-ba13-1cd7897d2359)
데이터 전처리 및 학습을 하기 위해 AI서버를 사용하였다. AI서버란 인공지능 및 머신러닝 작업을 수행하기 위해 고성능 그래픽장치(GPU)를 장착한 서버로 이미지 Segmentation과 같이 대규모 데이터를 학습하는데 적합하다. AI서버를 효과적으로 사용하기 위해 기존의 아나콘다 환경이 아닌 쿠버네티스 플랫폼을 사용하여 진행하였다.
![nnUNet](https://github.com/pnucse-capstone/capstone-2023-1-01/assets/48307605/e3b654dd-a025-4471-afbd-e4a583505bba)
기존의 의료영상데이터를 다루는 모델에는 서로 다른 장기간의 segmentation방식에 큰 차이가 있었고 표준화된 방식이 없었다. 이를 해결하고자 다양한 데이터에 대해 표준화된 파이프라인을 제공하는 nnUNet이 만들어지게 되었고, nnUNet을 사용하여 데이터 전처리 및 학습을 진행하였다. 학습된 데이터를 성능평가지표인 DSC와 NSD를 통해 평가하였다.

### 3.3 시각화 프로그램


## 4. 소개 및 시연 영상

프로젝트 소개나 시연 영상을 넣으세요.

## 5. 설치 및 사용법
본 프로젝트는 Ubuntu 20.04 버전에서 개발되었으며 함께 포함된 다음의 스크립트를 수행하여 관련 패키지들의 설치와 빌드를 수행할 수 있습니다.
### 환경
- Python 3.8.2
- Driver version 510.47.03
- CUDA Version 11.6
- Docker 20.10.12
  
### Train Models
- MIC-DKFZ
  - nnUNet(https://github.com/MIC-DKFZ/nnUNet)
 
### Dataset
- AbdomenCT-1K Dataset
  - part1(https://zenodo.org/record/5903099)
  - part2(https://zenodo.org/record/5903846)
  - part3(https://zenodo.org/record/5903769)

## 4. README.md 작성팁 
* 마크다운 언어를 이용해 README.md 파일을 작성할 때 참고할 수 있는 마크다운 언어 문법을 공유합니다.  
* 다양한 예제와 보다 자세한 문법은 [이 문서](https://www.markdownguide.org/basic-syntax/)를 참고하세요.

### 4.1. 텍스트 추가
```markdown
본문입니다.

# This is a Header 1
## This is a Header 2
### This is a Header 3
#### This is a Header 4
##### This is a Header 5
###### This is a Header 6

**bold**
_italic_
`code`

1. Ordered
2. List

* Unordered 
* List

<!--주석-->

[link text](URL)
```

### 4.2. 이미지 추가

```markdown
<!--![이미지 이름](이미지 URL 링크)-->
![정보융합공학과 이미지](https://user-images.githubusercontent.com/100384365/192478661-5dc79a18-b076-48ef-b842-bcf65b0d8d44.jpg)
```

![정보융합공학과 이미지](https://user-images.githubusercontent.com/100384365/192478661-5dc79a18-b076-48ef-b842-bcf65b0d8d44.jpg)

이 때, 이미지 URL은 아래와 같이 github issue를 통해 image file만을 github server에 업로드하고 URL을 얻을 수 있습니다. (URL만 copy하고 issue 제출 X)

![이미지 URL 얻기1](https://user-images.githubusercontent.com/113662020/193720098-9f19831b-7107-4a91-9821-a977ff82e8de.png)
![이미지 URL 얻기2](https://user-images.githubusercontent.com/113662020/193720141-8b813247-b77b-4590-83cc-f87a4e63296b.png)

### 4.3. 유튜브 영상 추가
```markdown
<!--[![영상 이름](유튜브 영상 썸네일 URL)](유투브 영상 URL)-->
[![부산대학교 정보컴퓨터공학부 소개](http://img.youtube.com/vi/zh_gQ_lmLqE/0.jpg)](https://www.youtube.com/watch?v=zh_gQ_lmLqE)    
```
[![부산대학교 정보컴퓨터공학부 소개](http://img.youtube.com/vi/zh_gQ_lmLqE/0.jpg)](https://www.youtube.com/watch?v=zh_gQ_lmLqE)    

이때 유투브 영상 썸네일 URL은 유투브 영상 URL로부터 다음과 같이 얻을 수 있습니다.

Youtube URL: https://www.youtube.com/watch?v={동영상 ID}

Youtube Thumbnail URL: http://img.youtube.com/vi/{동영상 ID}/0.jpg 

예를 들어, https://www.youtube.com/watch?v=zh_gQ_lmLqE 라고 하면 썸네일의 주소는 http://img.youtube.com/vi/zh_gQ_lmLqE/0.jpg 이다.





