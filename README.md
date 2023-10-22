# Capstone-2022-1-05



### 1. 프로젝트 소개

프로젝트 명, 목적, 개요 등 프로젝트에 대한 간단한 소개글을 작성하세요.

### 2. 팀 소개

프로젝트에 참여한 팀원들의 이름, 이메일, 역할를 포함해 팀원들을 소개하세요.

### 3. 시스템 구성도

프로젝트 결과물의 개괄적인 동작을 파악할 수 있는 이미지와 글을 작성하세요.

### 4. 소개 및 시연 영상

프로젝트 소개나 시연 영상을 넣으세요.

### 5. 설치 및 사용법
본 프로젝트는 Ubuntu 20.04 버전에서 개발되었으며 함께 포함된 다음의 스크립트를 수행하여 관련 패키지들의 설치와 빌드를 수행할 수 있습니다.
### 환경
- Python 3.8.2
- docker 20.10.12
### Train Models
- MIC-DKFZ
  - nnUNet(https://github.com/MIC-DKFZ/nnUNet)

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





