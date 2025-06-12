"""
프로토타입용 인재 데이터베이스
시나리오 테스트용 실제 데이터
"""

from typing import Dict, List, Optional

class TalentDatabase:
    """인재 데이터베이스 클래스"""
    
    def __init__(self):
        self.talents = self._generate_scenario_data()
        print(f"👥 시나리오 테스트용 인재 데이터 생성: {len(self.talents)}명")
    
    def _generate_scenario_data(self) -> List[Dict]:
        """시나리오 테스트용 실제 인재 데이터"""
        talents = []
        
        # 시나리오 1 & 2: 금융 인프라 NE 인재들
        talents.extend([
            {
                "id": "SCENARIO1_001",
                "name": "김철수",
                "age_min": None,
                "age_max": None,
                "age": None,
                "residence": None,
                "final_education": None,
                "industry_domain": "금융",
                "industry_knowledge": "인프라",
                "industry_detail": None,
                "specialization": "NE",
                "experience_years": 4,
                "talent_level": None,
                "skills": ["화웨이", "네트워크 유지보수"],
                "certifications": None,
                "other_skills": None,
                "vector_fields": {
                    "professional_competency": "화웨이 네트워크 유지보수 4년",
                    "technical_expertise": "화웨이 장비 전문",
                    "leadership_experience": None,
                    "scale_complexity": "중소 규모 유지보수 경험",
                    "compliance_security": None,
                    "industry_specialization": "금융 인프라"
                }
            },
            {
                "id": "SCENARIO1_002",
                "name": "이영희",
                "age_min": None,
                "age_max": None,
                "age": None,
                "residence": None,
                "final_education": None,
                "industry_domain": "금융",
                "industry_knowledge": "인프라",
                "industry_detail": None,
                "specialization": "NE",
                "experience_years": 5,
                "talent_level": None,
                "skills": ["시스코", "네트워크", "장비 구축"],
                "certifications": None,
                "other_skills": None,
                "vector_fields": {
                    "professional_competency": "시스코 네트워크 장비 구축 3년, 유지보수 2년",
                    "technical_expertise": "시스코 네트워크 전문",
                    "leadership_experience": "금융 인프라 구축 주도",
                    "scale_complexity": "중규모 프로젝트 참여 경험",
                    "compliance_security": None,
                    "industry_specialization": "금융 인프라"
                }
            },
            {
                "id": "SCENARIO1_003",
                "name": "박민수",
                "age_min": None,
                "age_max": None,
                "age": None,
                "residence": None,
                "final_education": None,
                "industry_domain": "금융",
                "industry_knowledge": "인프라",
                "industry_detail": None,
                "specialization": "SE",  # NE가 아닌 SE로 필터링 대상
                "experience_years": 3,
                "talent_level": None,
                "skills": ["java", "스프링"],
                "certifications": None,
                "other_skills": None,
                "vector_fields": {
                    "professional_competency": "리눅스 기반 정기점검 및 설치 보조 경험",
                    "technical_expertise": "Java 개발",
                    "leadership_experience": "금융권 현장 대응",
                    "scale_complexity": "소규모 인프라 유지보수",
                    "compliance_security": None,
                    "industry_specialization": "금융 인프라"
                }
            }
        ])
        
        # 시나리오 3: 에너지 SE 인재들
        talents.extend([
            {
                "id": "SCENARIO3_001",
                "name": "김철수",
                "age_min": None,
                "age_max": None,
                "age": None,
                "residence": None,
                "final_education": None,
                "industry_domain": "에너지",
                "industry_knowledge": None,
                "industry_detail": None,
                "specialization": "SE",
                "experience_years": 7,
                "talent_level": None,
                "skills": ["RedHat", "x86 서버", "Tomcat", "nginx", "이중화"],
                "certifications": ["RHCSA"],
                "other_skills": None,
                "vector_fields": {
                    "professional_competency": "RedHat 리눅스 기반 시스템 운영 및 이중화 경험, x86 서버 및 Tomcat, nginx 운영 경험",
                    "technical_expertise": "RedHat Linux 전문, 서버 운영",
                    "leadership_experience": None,
                    "scale_complexity": "중규모 SE 운영 프로젝트",
                    "compliance_security": None,
                    "industry_specialization": "에너지"
                }
            },
            {
                "id": "SCENARIO3_002",
                "name": "이영희",
                "age_min": None,
                "age_max": None,
                "age": None,
                "residence": None,
                "final_education": None,
                "industry_domain": "에너지",
                "industry_knowledge": None,
                "industry_detail": None,
                "specialization": "SE",
                "experience_years": 6,
                "talent_level": None,
                "skills": ["RedHat", "AIX", "가상화", "Tomcat"],
                "certifications": ["RHCA"],
                "other_skills": None,
                "vector_fields": {
                    "professional_competency": "RedHat 운영 및 가상화 경험 풍부",
                    "technical_expertise": "RedHat, AIX, 가상화 전문",
                    "leadership_experience": None,
                    "scale_complexity": "중대형 시스템 유지보수",
                    "compliance_security": None,
                    "industry_specialization": "에너지"
                }
            },
            {
                "id": "SCENARIO3_003",
                "name": "박민수",
                "age_min": None,
                "age_max": None,
                "age": None,
                "residence": None,
                "final_education": None,
                "industry_domain": "에너지",
                "industry_knowledge": None,
                "industry_detail": None,
                "specialization": "SE",
                "experience_years": 3,  # 경력 부족으로 필터링될 대상
                "talent_level": None,
                "skills": ["nginx", "오픈소스 운영", "가상화"],
                "certifications": None,
                "other_skills": None,
                "vector_fields": {
                    "professional_competency": "Tomcat, nginx 운영 및 오픈소스 경험",
                    "technical_expertise": "nginx, 오픈소스 운영",
                    "leadership_experience": None,
                    "scale_complexity": "중규모 서버 운영",
                    "compliance_security": None,
                    "industry_specialization": "에너지"
                }
            }
        ])
        
        # 시나리오 4: 금융 보험 SI/SM 인재들
        talents.extend([
            {
                "id": "SCENARIO4_001",
                "name": "김철수",
                "age_min": None,
                "age_max": None,
                "age": 38,
                "residence": None,
                "final_education": None,
                "industry_domain": "금융",
                "industry_knowledge": "보험",
                "industry_detail": None,
                "specialization": "SI",
                "experience_years": 11,
                "talent_level": "고급",
                "skills": ["Java", "Spring"],
                "certifications": None,
                "other_skills": None,
                "vector_fields": {
                    "professional_competency": "보험 상품/청약 시스템 개선 SI 경력",
                    "technical_expertise": "Java, Spring 전문",
                    "leadership_experience": "팀 리딩 경험 있음",
                    "scale_complexity": "대형 시스템 리뉴얼 프로젝트 참여",
                    "compliance_security": None,
                    "industry_specialization": "금융 보험"
                }
            },
            {
                "id": "SCENARIO4_002",
                "name": "이영희",
                "age_min": None,
                "age_max": None,
                "age": 40,
                "residence": None,
                "final_education": None,
                "industry_domain": "금융",
                "industry_knowledge": "보험",
                "industry_detail": None,
                "specialization": "SM",
                "experience_years": 13,
                "talent_level": "고급",
                "skills": ["Java", "Spring", "NCRM"],
                "certifications": None,
                "other_skills": None,
                "vector_fields": {
                    "professional_competency": "기간계 시스템 운영 중심, 자동차/일반보험 유지보수",
                    "technical_expertise": "Java, Spring, NCRM 전문",
                    "leadership_experience": "금융권 현장 대응",
                    "scale_complexity": "중규모 SM 유지보수 경험",
                    "compliance_security": None,
                    "industry_specialization": "금융 보험"
                }
            },
            {
                "id": "SCENARIO4_003",
                "name": "박민수",
                "age_min": None,
                "age_max": None,
                "age": 42,
                "residence": None,
                "final_education": None,
                "industry_domain": "금융",
                "industry_knowledge": "보험",
                "industry_detail": None,
                "specialization": "SM",
                "experience_years": 15,
                "talent_level": "무관",
                "skills": ["Java", "NCRM"],
                "certifications": None,
                "other_skills": None,
                "vector_fields": {
                    "professional_competency": "자동차/일반보험 SM 유지보수",
                    "technical_expertise": "Java, NCRM 전문",
                    "leadership_experience": None,
                    "scale_complexity": "중규모 보험 시스템",
                    "compliance_security": None,
                    "industry_specialization": "금융 보험"
                }
            }
        ])
        
        return talents
    
    def get_all_talents(self) -> List[Dict]:
        """모든 인재 정보 반환"""
        return self.talents.copy()
    
    def get_talent_by_id(self, talent_id: str) -> Optional[Dict]:
        """ID로 특정 인재 조회"""
        for talent in self.talents:
            if talent.get("id") == talent_id:
                return talent.copy()
        return None
    
    def get_talents_by_filter(self, filters: Dict) -> List[Dict]:
        """필터 조건으로 인재 검색"""
        filtered_talents = []
        
        for talent in self.talents:
            match = True
            
            for key, value in filters.items():
                if key in talent:
                    if isinstance(value, list):
                        if talent[key] not in value:
                            match = False
                            break
                    else:
                        if talent[key] != value:
                            match = False
                            break
            
            if match:
                filtered_talents.append(talent.copy())
        
        return filtered_talents
    
    def get_statistics(self) -> Dict:
        """인재 통계 정보"""
        stats = {
            "total_count": len(self.talents),
            "by_specialization": {},
            "by_residence": {},
            "by_industry": {},
            "by_talent_level": {},
            "experience_distribution": {
                "0-2년": 0,
                "3-5년": 0,
                "6-10년": 0,
                "11년+": 0
            }
        }
        
        for talent in self.talents:
            # 전문분야별
            spec = talent.get("specialization", "Unknown")
            stats["by_specialization"][spec] = stats["by_specialization"].get(spec, 0) + 1
            
            # 지역별
            residence = talent.get("residence", "Unknown")
            stats["by_residence"][residence] = stats["by_residence"].get(residence, 0) + 1
            
            # 산업별
            industry = talent.get("industry_domain", "Unknown")
            stats["by_industry"][industry] = stats["by_industry"].get(industry, 0) + 1
            
            # 등급별
            level = talent.get("talent_level", "Unknown")
            stats["by_talent_level"][level] = stats["by_talent_level"].get(level, 0) + 1
            
            # 경력별
            exp = talent.get("experience_years", 0)
            if exp <= 2:
                stats["experience_distribution"]["0-2년"] += 1
            elif exp <= 5:
                stats["experience_distribution"]["3-5년"] += 1
            elif exp <= 10:
                stats["experience_distribution"]["6-10년"] += 1
            else:
                stats["experience_distribution"]["11년+"] += 1
        
        return stats
    
    def add_talent(self, talent_data: Dict) -> bool:
        """새 인재 추가"""
        if "id" not in talent_data:
            return False
        
        # 중복 ID 체크
        if any(t["id"] == talent_data["id"] for t in self.talents):
            return False
        
        self.talents.append(talent_data)
        return True
    
    def update_talent(self, talent_id: str, update_data: Dict) -> bool:
        """인재 정보 업데이트"""
        for i, talent in enumerate(self.talents):
            if talent["id"] == talent_id:
                self.talents[i].update(update_data)
                return True
        return False
    
    def delete_talent(self, talent_id: str) -> bool:
        """인재 정보 삭제"""
        for i, talent in enumerate(self.talents):
            if talent["id"] == talent_id:
                del self.talents[i]
                return True
        return False
