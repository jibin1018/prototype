"""
Payload 검색 모듈
구조화된 필드를 기반으로 1차 필터링 수행
"""

import json
from typing import Dict, List, Optional, Any
from example.talent_data import TalentDatabase

class PayloadSearcher:
    """Payload 기반 검색 클래스"""
    
    def __init__(self):
        self.talent_db = TalentDatabase()
        self.talents = self.talent_db.get_all_talents()
        
        print(f"📦 Payload 검색기 초기화 ({len(self.talents)}명 인재 데이터 로드)")
    
    def search(self, parsed_query: Dict) -> List[Dict]:
        """Payload 검색 실행"""
        print("📦 Payload 검색 시작")
        
        candidates = []
        
        for talent in self.talents:
            score = self._calculate_payload_score(talent, parsed_query)
            
            if score > 0:  # 최소 조건 만족
                talent_with_score = talent.copy()
                talent_with_score["payload_score"] = score
                candidates.append(talent_with_score)
        
        # 점수 순으로 정렬
        candidates.sort(key=lambda x: x["payload_score"], reverse=True)
        
        print(f"✅ Payload 검색 완료: {len(candidates)}명 후보 선정")
        return candidates
    
    def _calculate_payload_score(self, talent: Dict, query: Dict) -> float:
        """Payload 매칭 점수 계산"""
        total_score = 0.0
        max_possible_score = 0.0
        
        # 1. 나이 매칭
        age_score, age_max = self._match_age(talent, query)
        total_score += age_score
        max_possible_score += age_max
        
        # 2. 거주지역 매칭
        residence_score, residence_max = self._match_residence(talent, query)
        total_score += residence_score
        max_possible_score += residence_max
        
        # 3. 산업 도메인 매칭
        industry_score, industry_max = self._match_industry_domain(talent, query)
        total_score += industry_score
        max_possible_score += industry_max
        
        # 4. 산업 지식 매칭
        knowledge_score, knowledge_max = self._match_industry_knowledge(talent, query)
        total_score += knowledge_score
        max_possible_score += knowledge_max
        
        # 5. 전문 분야 매칭
        spec_score, spec_max = self._match_specialization(talent, query)
        total_score += spec_score
        max_possible_score += spec_max
        
        # 6. 경력 매칭
        exp_score, exp_max = self._match_experience(talent, query)
        total_score += exp_score
        max_possible_score += exp_max
        
        # 7. 인재 등급 매칭
        level_score, level_max = self._match_talent_level(talent, query)
        total_score += level_score
        max_possible_score += level_max
        
        # 8. 기술 스택 매칭
        skills_score, skills_max = self._match_skills(talent, query)
        total_score += skills_score
        max_possible_score += skills_max
        
        # 정규화된 점수 반환 (0~1)
        if max_possible_score > 0:
            return total_score / max_possible_score
        else:
            return 0.0
    
    def _match_age(self, talent: Dict, query: Dict) -> tuple:
        """나이 매칭"""
        weight = 10.0
        
        talent_age = talent.get("age")
        if not talent_age:
            return 0.0, weight
        
        query_age = query.get("age")
        query_age_min = query.get("age_min")
        query_age_max = query.get("age_max")
        
        # 정확한 나이 매칭
        if query_age and talent_age == query_age:
            return weight, weight
        
        # 나이 범위 매칭
        if query_age_min or query_age_max:
            min_age = query_age_min or 0
            max_age = query_age_max or 100
            
            if min_age <= talent_age <= max_age:
                # 범위 중앙에 가까울수록 높은 점수
                center = (min_age + max_age) / 2
                distance = abs(talent_age - center)
                range_size = max_age - min_age
                
                if range_size > 0:
                    score = weight * (1 - distance / (range_size / 2))
                    return max(0, score), weight
                else:
                    return weight, weight
        
        return 0.0, weight
    
    def _match_residence(self, talent: Dict, query: Dict) -> tuple:
        """거주지역 매칭"""
        weight = 15.0
        
        talent_residence = talent.get("residence")
        query_residence = query.get("residence")
        
        if not query_residence:
            return weight * 0.5, weight  # 조건 없으면 중간 점수
        
        if not talent_residence:
            return 0.0, weight
        
        if talent_residence == query_residence:
            return weight, weight
        
        # 인접 지역 점수 (예: 서울-경기도)
        adjacent_regions = {
            "서울": ["경기도"],
            "경기도": ["서울", "인천"],
            "인천": ["경기도"]
        }
        
        if query_residence in adjacent_regions.get(talent_residence, []):
            return weight * 0.7, weight
        
        return 0.0, weight
    
    def _match_industry_domain(self, talent: Dict, query: Dict) -> tuple:
        """산업 도메인 매칭"""
        weight = 20.0
        
        talent_industry = talent.get("industry_domain")
        query_industry = query.get("industry_domain")
        
        if not query_industry:
            return weight * 0.5, weight
        
        if not talent_industry:
            return 0.0, weight
        
        if talent_industry == query_industry:
            return weight, weight
        
        # 유사 산업 점수
        similar_industries = {
            "금융": ["공공"],
            "공공": ["금융"],
            "제조": ["유통"],
            "유통": ["제조"]
        }
        
        if query_industry in similar_industries.get(talent_industry, []):
            return weight * 0.6, weight
        
        return 0.0, weight
    
    def _match_industry_knowledge(self, talent: Dict, query: Dict) -> tuple:
        """산업 지식 매칭"""
        weight = 15.0
        
        talent_knowledge = talent.get("industry_knowledge")
        query_knowledge = query.get("industry_knowledge")
        
        if not query_knowledge:
            return weight * 0.5, weight
        
        if not talent_knowledge:
            return 0.0, weight
        
        if talent_knowledge == query_knowledge:
            return weight, weight
        
        # 관련 지식 점수
        related_knowledge = {
            "인프라": ["네트워크", "시스템"],
            "은행": ["금융", "보험"],
            "증권": ["금융", "투자"]
        }
        
        talent_knowledge_list = talent_knowledge if isinstance(talent_knowledge, list) else [talent_knowledge]
        
        for tk in talent_knowledge_list:
            if query_knowledge in related_knowledge.get(tk, []) or tk == query_knowledge:
                return weight * 0.8, weight
        
        return 0.0, weight
    
    def _match_specialization(self, talent: Dict, query: Dict) -> tuple:
        """전문 분야 매칭"""
        weight = 25.0
        
        talent_spec = talent.get("specialization")
        query_spec = query.get("specialization")
        
        if not query_spec:
            return weight * 0.5, weight
        
        if not talent_spec:
            return 0.0, weight
        
        if talent_spec == query_spec:
            return weight, weight
        
        # 관련 전문 분야 점수
        related_specs = {
            "NE": ["SE", "보안"],
            "SE": ["NE", "OP"],
            "DBA": ["DVLP", "AA"],
            "DVLP": ["DBA", "AA"],
            "보안": ["NE", "SE"]
        }
        
        if query_spec in related_specs.get(talent_spec, []):
            return weight * 0.7, weight
        
        return 0.0, weight
    
    def _match_experience(self, talent: Dict, query: Dict) -> tuple:
        """경력 매칭"""
        weight = 20.0
        
        talent_exp = talent.get("experience_years")
        query_exp = query.get("experience_years")
        
        if not query_exp:
            return weight * 0.5, weight
        
        if not talent_exp:
            return 0.0, weight
        
        # 경력 요구사항 이상인지 확인
        if talent_exp >= query_exp:
            # 과도한 경력은 점수 조정 (오버스펙)
            if talent_exp <= query_exp * 2:
                return weight, weight
            else:
                # 오버스펙 패널티
                return weight * 0.8, weight
        else:
            # 경력 부족
            shortage = query_exp - talent_exp
            if shortage <= 1:
                return weight * 0.6, weight
            else:
                return 0.0, weight
    
    def _match_talent_level(self, talent: Dict, query: Dict) -> tuple:
        """인재 등급 매칭"""
        weight = 15.0
        
        talent_level = talent.get("talent_level")
        query_levels = query.get("talent_level")
        
        if not query_levels:
            return weight * 0.5, weight
        
        if not talent_level:
            return 0.0, weight
        
        if isinstance(query_levels, list):
            if talent_level in query_levels or "등급무관" in query_levels:
                return weight, weight
        else:
            if talent_level == query_levels or query_levels == "등급무관":
                return weight, weight
        
        # 레벨 호환성 체크
        level_compatibility = {
            "고급": ["중급"],
            "중급": ["고급", "초급"]
        }
        
        compatible_levels = level_compatibility.get(talent_level, [])
        if any(level in compatible_levels for level in (query_levels if isinstance(query_levels, list) else [query_levels])):
            return weight * 0.7, weight
        
        return 0.0, weight
    
    def _match_skills(self, talent: Dict, query: Dict) -> tuple:
        """기술 스택 매칭"""
        weight = 30.0
        
        talent_skills = talent.get("skills", [])
        query_skills = query.get("skills", [])
        
        if not query_skills:
            return weight * 0.5, weight
        
        if not talent_skills:
            return 0.0, weight
        
        # 기술 스택 교집합 계산
        talent_skills_lower = [skill.lower() for skill in talent_skills]
        query_skills_lower = [skill.lower() for skill in query_skills]
        
        matches = set(talent_skills_lower) & set(query_skills_lower)
        
        if matches:
            match_ratio = len(matches) / len(query_skills_lower)
            return weight * match_ratio, weight
        
        # 유사 기술 매칭
        similar_skills = {
            "linux": ["unix", "centos", "ubuntu"],
            "oracle": ["mysql", "postgresql"],
            "java": ["spring", "jsp"],
            "aws": ["azure", "gcp"]
        }
        
        similar_matches = 0
        for query_skill in query_skills_lower:
            for talent_skill in talent_skills_lower:
                if talent_skill in similar_skills.get(query_skill, []):
                    similar_matches += 1
                    break
        
        if similar_matches > 0:
            similar_ratio = similar_matches / len(query_skills_lower)
            return weight * similar_ratio * 0.7, weight
        
        return 0.0, weight
    
    def filter_by_mandatory_requirements(self, candidates: List[Dict], mandatory_fields: List[str]) -> List[Dict]:
        """필수 요구사항 필터링"""
        
        if not mandatory_fields:
            return candidates
        
        filtered = []
        
        for candidate in candidates:
            meets_all_mandatory = True
            
            for field in mandatory_fields:
                if not candidate.get(field):
                    meets_all_mandatory = False
                    break
            
            if meets_all_mandatory:
                filtered.append(candidate)
        
        print(f"📦 필수 요구사항 필터링: {len(filtered)}명 잔여")
        return filtered
    
    def get_search_statistics(self, candidates: List[Dict]) -> Dict:
        """검색 통계 정보 반환"""
        
        if not candidates:
            return {"total": 0}
        
        stats = {
            "total": len(candidates),
            "avg_score": sum(c["payload_score"] for c in candidates) / len(candidates),
            "top_score": max(c["payload_score"] for c in candidates),
            "by_specialization": {},
            "by_residence": {},
            "by_talent_level": {}
        }
        
        # 전문분야별 분포
        for candidate in candidates:
            spec = candidate.get("specialization", "Unknown")
            stats["by_specialization"][spec] = stats["by_specialization"].get(spec, 0) + 1
        
        # 지역별 분포
        for candidate in candidates:
            residence = candidate.get("residence", "Unknown")
            stats["by_residence"][residence] = stats["by_residence"].get(residence, 0) + 1
        
        # 등급별 분포
        for candidate in candidates:
            level = candidate.get("talent_level", "Unknown")
            stats["by_talent_level"][level] = stats["by_talent_level"].get(level, 0) + 1
        
        return stats