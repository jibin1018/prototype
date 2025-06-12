"""
동적 가중치 컨트롤러
사용자 입력에 따라 검색 가중치를 동적으로 조정
"""

from typing import Dict, List, Optional
import math
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

class WeightController:
    """동적 가중치 컨트롤러"""
    
    def __init__(self):
        # 기본 가중치 설정
        self.default_weights = {
            "age": 0.15,
            "residence": 0.20,
            "industry_domain": 0.25,
            "industry_knowledge": 0.20,
            "specialization": 0.30,
            "experience_years": 0.25,
            "talent_level": 0.20,
            "skills": 0.35,
            "vector_fields": {
                "professional_competency": 0.25,
                "technical_expertise": 0.30,
                "leadership_experience": 0.15,
                "scale_complexity": 0.10,
                "compliance_security": 0.15,
                "industry_specialization": 0.20
            }
        }
        
        print("⚖️  동적 가중치 컨트롤러 초기화 완료")
    
    def calculate_weights(self, parsed_query: Dict) -> Dict:
        """파싱된 쿼리 기반 동적 가중치 계산"""
        logger.info("⚖️  동적 가중치 계산 시작")
        
        try:
            # 기본 가중치 복사 (깊은 복사)
            weights = {}
            for key, value in self.default_weights.items():
                if key == "vector_fields":
                    weights[key] = value.copy()
                else:
                    weights[key] = value
            
            # 1. 필드별 존재 여부에 따른 가중치 조정
            weights = self._adjust_by_field_presence(weights, parsed_query)
            
            # 2. 우선순위 키워드에 따른 가중치 부스팅
            weights = self._adjust_by_priority_keywords(weights, parsed_query)
            
            # 3. 산업별 특성 반영
            weights = self._adjust_by_industry_characteristics(weights, parsed_query)
            
            # 4. 경력 수준에 따른 조정
            weights = self._adjust_by_experience_level(weights, parsed_query)
            
            # 5. 가중치 정규화
            weights = self._normalize_weights(weights)
            
            logger.info("✅ 동적 가중치 계산 완료")
            return weights
            
        except Exception as e:
            logger.error(f"❌ 가중치 계산 오류: {e}")
            return self.default_weights.copy()
    
    def _adjust_by_field_presence(self, weights: Dict, parsed_query: Dict) -> Dict:
        """필드 존재 여부에 따른 가중치 조정"""
        try:
            # 명시적으로 언급된 필드의 가중치 증가
            boost_factor = 1.3
            reduce_factor = 0.8
            
            # 나이 관련
            if any([parsed_query.get("age"), parsed_query.get("age_min"), parsed_query.get("age_max")]):
                weights["age"] *= boost_factor
            else:
                weights["age"] *= reduce_factor
            
            # 거주지역
            if parsed_query.get("residence"):
                weights["residence"] *= boost_factor
            else:
                weights["residence"] *= reduce_factor
            
            # 산업 분야
            if parsed_query.get("industry_domain"):
                weights["industry_domain"] *= boost_factor
                
            # 전문 분야
            if parsed_query.get("specialization"):
                weights["specialization"] *= boost_factor
            
            # 경력
            if parsed_query.get("experience_years"):
                weights["experience_years"] *= boost_factor
            
            # 기술 스택
            if parsed_query.get("skills"):
                weights["skills"] *= boost_factor
                
            # 인재 등급
            if parsed_query.get("talent_level"):
                weights["talent_level"] *= boost_factor
                
        except Exception as e:
            logger.warning(f"필드 존재 여부 조정 오류: {e}")
        
        return weights
    
    def _adjust_by_priority_keywords(self, weights: Dict, parsed_query: Dict) -> Dict:
        """우선순위 키워드에 따른 가중치 조정"""
        try:
            # 긴급 키워드 감지 (requirement_type에서 확인)
            req_types = parsed_query.get("requirement_type", [])
            if "긴급" in req_types:
                # 긴급시 기술 스택과 전문성 가중치 증가
                weights["skills"] *= 1.4
                weights["specialization"] *= 1.3
                weights["vector_fields"]["technical_expertise"] *= 1.3
            
            # 고급 인재 키워드
            talent_levels = parsed_query.get("talent_level", [])
            if isinstance(talent_levels, list) and "고급" in talent_levels:
                weights["vector_fields"]["technical_expertise"] *= 1.4
                weights["vector_fields"]["leadership_experience"] *= 1.3
                weights["experience_years"] *= 1.2
            elif isinstance(talent_levels, str) and "고급" in talent_levels:
                weights["vector_fields"]["technical_expertise"] *= 1.4
                weights["vector_fields"]["leadership_experience"] *= 1.3
                weights["experience_years"] *= 1.2
                
        except Exception as e:
            logger.warning(f"우선순위 키워드 조정 오류: {e}")
        
        return weights
    
    def _adjust_by_industry_characteristics(self, weights: Dict, parsed_query: Dict) -> Dict:
        """산업별 특성에 따른 가중치 조정"""
        try:
            industry = parsed_query.get("industry_domain")
            
            if industry == "금융":
                # 금융권은 보안과 컴플라이언스 중요
                weights["vector_fields"]["compliance_security"] *= 1.5
                weights["vector_fields"]["industry_specialization"] *= 1.3
                
            elif industry == "공공":
                # 공공은 안정성과 컴플라이언스 중요
                weights["vector_fields"]["compliance_security"] *= 1.4
                weights["experience_years"] *= 1.2
                
            elif industry == "제조":
                # 제조업은 실무 경험과 안정성 중요
                weights["vector_fields"]["professional_competency"] *= 1.3
                weights["vector_fields"]["scale_complexity"] *= 1.2
                
            elif industry == "유통":
                # 유통은 확장성과 성능 중요
                weights["vector_fields"]["scale_complexity"] *= 1.4
                weights["skills"] *= 1.2
                
            elif industry == "에너지":
                # 에너지는 시스템 안정성과 운영 경험 중요
                weights["vector_fields"]["professional_competency"] *= 1.3
                weights["vector_fields"]["scale_complexity"] *= 1.2
                
        except Exception as e:
            logger.warning(f"산업별 특성 조정 오류: {e}")
        
        return weights
    
    def _adjust_by_experience_level(self, weights: Dict, parsed_query: Dict) -> Dict:
        """경력 수준에 따른 가중치 조정"""
        try:
            experience = parsed_query.get("experience_years")
            
            if experience:
                if experience >= 10:
                    # 10년 이상 경력자는 리더십과 복잡성 중요
                    weights["vector_fields"]["leadership_experience"] *= 1.4
                    weights["vector_fields"]["scale_complexity"] *= 1.3
                    
                elif experience >= 5:
                    # 5년 이상은 기술 전문성 중요
                    weights["vector_fields"]["technical_expertise"] *= 1.3
                    weights["skills"] *= 1.2
                    
                elif experience >= 2:
                    # 2년 이상은 전문 역량 중요
                    weights["vector_fields"]["professional_competency"] *= 1.2
                    
                else:
                    # 신입급은 기본 기술과 학습 능력
                    weights["skills"] *= 1.1
                    
        except Exception as e:
            logger.warning(f"경력 수준 조정 오류: {e}")
        
        return weights
    
    def _normalize_weights(self, weights: Dict) -> Dict:
        """가중치 정규화"""
        try:
            # 메인 필드 정규화
            main_fields = ["age", "residence", "industry_domain", "industry_knowledge", 
                          "specialization", "experience_years", "talent_level", "skills"]
            
            total_main = sum(weights.get(field, 0) for field in main_fields)
            
            if total_main > 0:
                for field in main_fields:
                    if field in weights:
                        weights[field] = weights[field] / total_main
            
            # 벡터 필드 정규화
            vector_fields = weights.get("vector_fields", {})
            total_vector = sum(vector_fields.values())
            
            if total_vector > 0:
                for field in vector_fields:
                    vector_fields[field] = vector_fields[field] / total_vector
                    
        except Exception as e:
            logger.warning(f"가중치 정규화 오류: {e}")
        
        return weights
    
    def get_field_importance(self, field_name: str, weights: Dict) -> float:
        """특정 필드의 중요도 반환"""
        try:
            if field_name in weights:
                return weights[field_name]
            elif field_name in weights.get("vector_fields", {}):
                return weights["vector_fields"][field_name]
            else:
                return 0.0
        except Exception:
            return 0.0
    
    def apply_custom_weights(self, base_weights: Dict, custom_adjustments: Dict) -> Dict:
        """사용자 정의 가중치 적용"""
        try:
            adjusted_weights = {}
            
            # 기본 가중치 복사
            for key, value in base_weights.items():
                if key == "vector_fields":
                    adjusted_weights[key] = value.copy()
                else:
                    adjusted_weights[key] = value
            
            # 커스텀 조정 적용
            for field, adjustment in custom_adjustments.items():
                if field in adjusted_weights:
                    adjusted_weights[field] *= adjustment
                elif field in adjusted_weights.get("vector_fields", {}):
                    adjusted_weights["vector_fields"][field] *= adjustment
            
            return self._normalize_weights(adjusted_weights)
            
        except Exception as e:
            logger.warning(f"커스텀 가중치 적용 오류: {e}")
            return base_weights
    
    def explain_weights(self, weights: Dict) -> Dict:
        """가중치 설정 이유 설명"""
        try:
            explanations = {
                "main_factors": [],
                "vector_factors": [],
                "adjustments": []
            }
            
            # 높은 가중치 필드 설명
            for field, weight in weights.items():
                if field != "vector_fields" and weight > 0.25:
                    explanations["main_factors"].append({
                        "field": field,
                        "weight": round(weight, 3),
                        "reason": self._get_weight_reason(field, weight)
                    })
            
            # 벡터 필드 설명
            vector_fields = weights.get("vector_fields", {})
            for field, weight in vector_fields.items():
                if weight > 0.2:
                    explanations["vector_factors"].append({
                        "field": field,
                        "weight": round(weight, 3),
                        "reason": self._get_vector_weight_reason(field, weight)
                    })
            
            return explanations
            
        except Exception as e:
            logger.warning(f"가중치 설명 오류: {e}")
            return {"error": "가중치 설명 생성 중 오류 발생"}
    
    def _get_weight_reason(self, field: str, weight: float) -> str:
        """가중치 설정 이유 반환"""
        reasons = {
            "skills": "명시된 기술 스택이 매칭의 핵심 요소",
            "specialization": "전문 분야가 명확히 지정됨",
            "industry_domain": "특정 산업 분야 요구사항",
            "experience_years": "경력 년수가 중요한 조건",
            "residence": "지역 제한이 있는 요구사항",
            "talent_level": "인재 등급이 명시됨"
        }
        
        return reasons.get(field, "높은 중요도로 설정됨")
    
    def _get_vector_weight_reason(self, field: str, weight: float) -> str:
        """벡터 가중치 설정 이유 반환"""
        reasons = {
            "technical_expertise": "기술 전문성이 핵심 요구사항",
            "professional_competency": "실무 역량이 중요한 요소",
            "industry_specialization": "해당 산업 전문성 필요",
            "leadership_experience": "리더십 경험이 요구됨",
            "scale_complexity": "대규모 시스템 경험 필요",
            "compliance_security": "보안 및 컴플라이언스 중요"
        }
        
        return reasons.get(field, "중요한 평가 요소")