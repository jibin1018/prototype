"""
규칙 기반 프롬프트 파서
기존 parser.py의 규칙 기반 로직을 활용하여 구현
"""

import json
import re
from typing import Dict, List, Optional
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RulebasePromptParser:
    """규칙 기반 프롬프트 파서 클래스"""
    
    def __init__(self):
        self.current_year = datetime.now().year
        self.mappings = self._init_mappings()
        print("📋 Rulebase 파서 초기화 완료")
    
    def _init_mappings(self) -> Dict:
        """매핑 테이블 초기화 - 실제 데이터에 맞게 수정"""
        return {
            "regions": {
                "서울": ["서울", "seoul", "강남", "강북", "마포", "용산", "강서", "송파"],
                "경기도": ["경기", "수원", "성남", "안양", "부천", "고양", "평택", "용인", "분당", "판교"],
                "부산": ["부산", "busan", "해운대", "남구", "동래"],
                "인천": ["인천", "incheon", "송도", "연수"],
                "대전": ["대전", "daejeon", "유성", "서구"],
                "대구": ["대구", "daegu", "수성", "달서"],
                "광주": ["광주", "gwangju", "북구", "서구"],
                "울산": ["울산", "ulsan", "남구", "동구"]
            },
            "industry_domains": {
                "금융": ["금융", "은행", "증권", "보험", "카드", "핀테크", "finance", "banking"],
                "공공": ["공공", "정부", "관공서", "공기업", "government"],
                "제조": ["제조", "manufacturing", "생산", "공장"],
                "유통": ["유통", "retail", "이커머스", "쇼핑몰", "물류"],
                "에너지": ["에너지", "전력", "발전", "한전", "전기"],
                "일반": ["일반", "기업", "회사"]
            },
            "industry_knowledge": {
                "인프라": ["인프라", "infrastructure", "서버", "네트워크"],
                "보험": ["보험", "insurance", "생보", "손보", "보험사"],
                "은행": ["은행", "banking", "여신", "수신"],
                "증권": ["증권", "securities", "투자", "자산관리"],
                "군업무": ["군", "국방", "military", "보안"],
                "메디컬": ["의료", "medical", "병원", "헬스케어"],
                "전력": ["전력", "전기", "power", "에너지"],
                "공통": ["공통", "일반", "범용"]
            },
            "specializations": {
                "NE": ["ne", "네트워크", "network", "스위치", "라우터", "시스코", "cisco"],
                "SE": ["se", "시스템", "system", "서버", "unix", "linux", "리눅스"],
                "DVLP": ["개발", "development", "프로그래밍", "코딩", "dev", "java", "spring"],
                "DBA": ["dba", "데이터베이스", "database", "db", "오라클", "mysql"],
                "보안": ["보안", "security", "정보보호", "해킹", "방화벽"],
                "AA": ["aa", "application", "어플리케이션", "앱", "아키텍처"],
                "PMO": ["pmo", "프로젝트", "project", "관리"],
                "OP": ["op", "운영", "operation", "모니터링", "시스템운영"],
                "QA": ["qa", "테스트", "test", "품질보증"],
                "WAS": ["was", "웹서버", "tomcat", "weblogic"],
                "회계": ["회계", "accounting", "재무", "세무"]
            },
            "talent_levels": {
                "고급": ["고급", "senior", "시니어", "전문가", "expert"],
                "중급": ["중급", "middle", "미들", "경력"],
                "초급": ["초급", "junior", "주니어", "신입", "entry"],
                "등급무관": ["등급무관", "무관", "상관없음"]
            },
            "tech_stacks": {
                "네트워크": ["cisco", "juniper", "hp", "switch", "router", "firewall", "시스코", "화웨이"],
                "서버OS": ["linux", "unix", "windows", "centos", "ubuntu", "redhat", "aix", "리눅스"],
                "데이터베이스": ["oracle", "mysql", "postgresql", "mssql", "mongodb", "오라클"],
                "개발언어": ["java", "python", "c++", "javascript", "php", "c#", "spring"],
                "클라우드": ["aws", "azure", "gcp", "docker", "kubernetes"],
                "보안": ["ips", "ids", "waf", "dlp", "apm", "방화벽"],
                "웹서버": ["apache", "nginx", "tomcat", "weblogic", "jboss"],
                "기타": ["ncrm", "가상화", "이중화", "dns", "proxy"]
            }
        }
    
    def parse(self, user_input: str) -> Dict:
        """메인 파싱 함수"""
        logger.info(f"📋 Rulebase 파싱 시작: {user_input}")
        
        try:
            result = self._create_empty_result()
            text = user_input.lower()
            
            # 1. 나이 정보 추출
            age_info = self._extract_age_info(text, user_input)
            result.update(age_info)
            
            # 2. 기본 정보 추출
            result["residence"] = self._find_best_match(text, "regions")
            result["industry_domain"] = self._find_best_match(text, "industry_domains")
            result["industry_knowledge"] = self._find_best_match(text, "industry_knowledge")
            result["specialization"] = self._find_best_match(text, "specializations")
            
            # 3. 경력 추출
            result["experience_years"] = self._extract_experience_years(text)
            
            # 4. 인재 등급 추출
            result["talent_level"] = self._extract_talent_levels(text)
            
            # 5. 기술 스택 추출
            result["skills"] = self._extract_tech_skills(text)
            
            # 6. 벡터 필드 생성
            result["vector_fields"] = self._generate_vector_fields(user_input, result)
            
            # 7. 조건 분류
            result["requirement_type"] = self._classify_requirements(text)
            
            # 8. 미분류 필드
            result["unknown_fields"] = self._extract_unknown_fields(text)
            
            logger.info("✅ Rulebase 파싱 완료")
            return result
            
        except Exception as e:
            logger.error(f"❌ 파싱 오류: {str(e)}")
            return self._create_empty_result()
    
    def _create_empty_result(self) -> Dict:
        """빈 결과 구조 생성"""
        return {
            "age_min": None,
            "age_max": None,
            "age": None,
            "residence": None,
            "industry_domain": None,
            "industry_knowledge": None,
            "specialization": None,
            "experience_years": None,
            "talent_level": None,
            "skills": None,
            "vector_fields": {
                "professional_competency": None,
                "technical_expertise": None,
                "leadership_experience": None,
                "scale_complexity": None,
                "compliance_security": None,
                "industry_specialization": None
            },
            "requirement_type": [],
            "unknown_fields": []
        }
    
    def _extract_age_info(self, text: str, original_text: str) -> Dict:
        """나이 정보 추출 - 완전한 버전"""
        age_info = {}
        
        try:
            # 구체적 나이 패턴
            age_patterns = [
                r'(\d{1,2})세',
                r'(\d{1,2})살',
                r'age\s*(\d{1,2})',
            ]
            
            for pattern in age_patterns:
                match = re.search(pattern, text)
                if match:
                    age = int(match.group(1))
                    if 20 <= age <= 65:
                        age_info["age"] = age
                        break
            
            # 나이 범위 패턴
            range_match = re.search(r'(\d{1,2})\s*~\s*(\d{1,2})세', text)
            if range_match:
                min_age = int(range_match.group(1))
                max_age = int(range_match.group(2))
                age_info["age_min"] = min_age
                age_info["age_max"] = max_age
            
            # 30대, 40대 등 처리
            decade_match = re.search(r'(\d{1})0대', text)
            if decade_match:
                decade = int(decade_match.group(1))
                if 2 <= decade <= 6:
                    age_info["age_min"] = decade * 10
                    age_info["age_max"] = decade * 10 + 9
            
            # 이상/이하 처리
            above_match = re.search(r'(\d{1,2})\s*이상', text)
            if above_match:
                age_info["age_min"] = int(above_match.group(1))
            
            below_match = re.search(r'(\d{1,2})\s*이하', text)
            if below_match:
                age_info["age_max"] = int(below_match.group(1))
                
        except ValueError as e:
            logger.warning(f"나이 파싱 오류: {e}")
        
        return age_info
    
    def _find_best_match(self, text: str, category: str) -> Optional[str]:
        """텍스트에서 카테고리별 최적 매칭"""
        try:
            mappings = self.mappings.get(category, {})
            
            for key, keywords in mappings.items():
                for keyword in keywords:
                    if keyword.lower() in text:
                        return key
        except Exception as e:
            logger.warning(f"매칭 오류 ({category}): {e}")
        
        return None
    
    def _extract_experience_years(self, text: str) -> Optional[int]:
        """경력년수 추출"""
        try:
            patterns = [
                r'(\d{1,2})\s*년\s*이상',
                r'(\d{1,2})\s*년차',
                r'경력\s*(\d{1,2})\s*년',
                r'(\d{1,2})\s*year',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    years = int(match.group(1))
                    if 0 <= years <= 30:
                        return years
        except ValueError as e:
            logger.warning(f"경력년수 파싱 오류: {e}")
        
        return None
    
    def _extract_talent_levels(self, text: str) -> Optional[List[str]]:
        """인재 등급 추출"""
        try:
            levels = []
            
            for level, keywords in self.mappings["talent_levels"].items():
                for keyword in keywords:
                    if keyword in text:
                        levels.append(level)
                        break
            
            return levels if levels else None
        except Exception as e:
            logger.warning(f"인재등급 파싱 오류: {e}")
            return None
    
    def _extract_tech_skills(self, text: str) -> Optional[List[str]]:
        """기술 스택 추출"""
        try:
            skills = []
            
            for category, tech_list in self.mappings["tech_stacks"].items():
                for tech in tech_list:
                    if tech.lower() in text:
                        skills.append(tech)
            
            return list(set(skills)) if skills else None
        except Exception as e:
            logger.warning(f"기술스택 파싱 오류: {e}")
            return None
    
    def _generate_vector_fields(self, original_text: str, parsed_data: Dict) -> Dict:
        """벡터 필드 생성"""
        vector_fields = {
            "professional_competency": None,
            "technical_expertise": None,
            "leadership_experience": None,
            "scale_complexity": None,
            "compliance_security": None,
            "industry_specialization": None
        }
        
        try:
            text = original_text.lower()
            
            # 전문 역량
            competencies = []
            competency_keywords = {
                "유지보수": ["유지보수", "maintenance", "운영", "관리"],
                "구축": ["구축", "설치", "구현", "개발", "설계"],
                "정기점검": ["점검", "모니터링", "감시"],
                "트러블슈팅": ["장애", "문제해결", "troubleshooting"],
                "시스템 운영": ["시스템 운영", "운영 경험"]
            }
            
            for comp, keywords in competency_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        competencies.append(comp)
                        break
            
            if competencies:
                vector_fields["professional_competency"] = ", ".join(competencies)
            
            # 기술 전문성
            if parsed_data.get("specialization"):
                spec_map = {
                    "NE": "네트워크 인프라 전문성",
                    "SE": "시스템 엔지니어링 전문성",
                    "DBA": "데이터베이스 관리 전문성",
                    "DVLP": "소프트웨어 개발 전문성",
                    "보안": "정보보안 전문성",
                    "OP": "시스템 운영 전문성",
                    "AA": "아키텍처 설계 전문성",
                    "PMO": "프로젝트 관리 전문성",
                    "QA": "품질관리 전문성",
                    "WAS": "웹서버 관리 전문성"
                }
                vector_fields["technical_expertise"] = spec_map.get(
                    parsed_data["specialization"], "기술 전문성"
                )
            
            # 산업 전문성
            if parsed_data.get("industry_domain"):
                industry_spec = f"{parsed_data['industry_domain']} 분야"
                if parsed_data.get("industry_knowledge"):
                    industry_spec += f", {parsed_data['industry_knowledge']} 전문성"
                vector_fields["industry_specialization"] = industry_spec
            
            # 규모/복잡성
            scale_keywords = ["대규모", "enterprise", "글로벌", "복잡한", "이중화", "클러스터"]
            for keyword in scale_keywords:
                if keyword in text:
                    vector_fields["scale_complexity"] = "대규모 시스템 경험"
                    break
            
            # 리더십
            leadership_keywords = ["팀장", "리더", "매니저", "관리", "lead", "주도"]
            for keyword in leadership_keywords:
                if keyword in text:
                    vector_fields["leadership_experience"] = "팀 리더십 경험"
                    break
            
            # 컴플라이언스/보안
            compliance_keywords = ["보안", "컴플라이언스", "규제", "인증", "감사"]
            for keyword in compliance_keywords:
                if keyword in text:
                    vector_fields["compliance_security"] = "보안/컴플라이언스 경험"
                    break
                    
        except Exception as e:
            logger.warning(f"벡터 필드 생성 오류: {e}")
        
        return vector_fields
    
    def _classify_requirements(self, text: str) -> List[str]:
        """요구사항 분류"""
        try:
            requirements = []
            
            req_keywords = {
                "긴급": ["긴급", "urgent", "즉시", "빨리"],
                "장기": ["장기", "long-term", "지속", "안정"],
                "프로젝트": ["프로젝트", "project", "구축"],
                "운영": ["운영", "operation", "유지보수"]
            }
            
            for req_type, keywords in req_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        requirements.append(req_type)
                        break
            
            return requirements
        except Exception as e:
            logger.warning(f"요구사항 분류 오류: {e}")
            return []
    
    def _extract_unknown_fields(self, text: str) -> List[str]:
        """미분류 필드 추출"""
        try:
            unknown_fields = []
            
            unknown_keywords = {
                "야간작업": ["야간", "night", "밤"],
                "출장가능": ["출장", "travel", "이동"],
                "상주근무": ["상주", "onsite", "현장"],
                "외근가능": ["외근", "field", "방문"],
                "원격근무": ["재택", "remote", "원격"]
            }
            
            for field, keywords in unknown_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        unknown_fields.append(field)
                        break
            
            return unknown_fields
        except Exception as e:
            logger.warning(f"미분류 필드 추출 오류: {e}")
            return []