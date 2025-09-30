#!/usr/bin/env python3
"""
Claude Optimization Automation Tool
כלי אוטומציה לעבודה מיטבית עם Claude API
"""

import os
import json
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

# הגדרת logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('claude_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ClaudeConfig:
    """קונפיגורציה עבור Claude API"""
    api_key: str
    model: str = "claude-opus-4-1-20250805"
    max_tokens: int = 4096
    temperature: float = 0.7
    top_p: float = 0.95
    retry_attempts: int = 3
    timeout: int = 60
    base_url: str = "https://api.anthropic.com/v1/messages"

class ClaudeOptimizer:
    """מחלקה ראשית לאופטימיזציה של Claude"""
    
    def __init__(self, api_key: str):
        self.config = ClaudeConfig(api_key=api_key)
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        })
        self.usage_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0
        }
        
    def send_message(self, 
                    prompt: str, 
                    system: Optional[str] = None,
                    max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """שליחת הודעה ל-Claude API"""
        
        messages = [{"role": "user", "content": prompt}]
        
        data = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": max_tokens or self.config.max_tokens,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p
        }
        
        if system:
            data["system"] = system
            
        for attempt in range(self.config.retry_attempts):
            try:
                response = self.session.post(
                    self.config.base_url,
                    json=data,
                    timeout=self.config.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self._update_usage_stats(result)
                    return result
                    
                logger.warning(f"API Error: {response.status_code} - {response.text}")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
                
        self.usage_stats["failed_requests"] += 1
        raise Exception("Failed to get response from Claude API")
        
    def _update_usage_stats(self, response: Dict[str, Any]):
        """עדכון סטטיסטיקות שימוש"""
        self.usage_stats["total_requests"] += 1
        self.usage_stats["successful_requests"] += 1
        
        if "usage" in response:
            tokens = response["usage"].get("total_tokens", 0)
            self.usage_stats["total_tokens"] += tokens
            # חישוב עלות משוער (דוגמה)
            self.usage_stats["total_cost"] += tokens * 0.00001
            
    def batch_process(self, prompts: List[str], 
                     system: Optional[str] = None,
                     max_workers: int = 5) -> List[Dict[str, Any]]:
        """עיבוד מקבילי של מספר פרומפטים"""
        
        logger.info(f"Starting batch processing of {len(prompts)} prompts")
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.send_message, prompt, system): i 
                for i, prompt in enumerate(prompts)
            }
            
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    result = future.result()
                    results.append((idx, result))
                except Exception as e:
                    logger.error(f"Failed to process prompt {idx}: {e}")
                    results.append((idx, None))
                    
        # סידור התוצאות לפי הסדר המקורי
        results.sort(key=lambda x: x[0])
        return [r[1] for r in results]
        
    def generate_content(self, 
                        content_type: str,
                        topic: str,
                        requirements: Optional[Dict] = None) -> str:
        """יצירת תוכן אוטומטית לפי סוג ונושא"""
        
        templates = {
            "blog_post": """Write a comprehensive blog post about {topic}.
                Requirements: {requirements}
                Include: engaging title, introduction, main points, conclusion, and CTA.""",
                
            "code": """Generate production-ready code for {topic}.
                Requirements: {requirements}
                Include: documentation, error handling, and best practices.""",
                
            "analysis": """Provide a detailed analysis of {topic}.
                Requirements: {requirements}
                Include: data insights, recommendations, and action items.""",
                
            "marketing": """Create marketing content for {topic}.
                Requirements: {requirements}
                Include: headlines, value propositions, and call-to-action."""
        }
        
        prompt = templates.get(content_type, "Generate content about {topic}")
        prompt = prompt.format(
            topic=topic,
            requirements=json.dumps(requirements or {})
        )
        
        response = self.send_message(prompt)
        return response["content"][0]["text"]
        
    def optimize_prompt(self, 
                        original_prompt: str,
                        optimization_goal: str = "clarity") -> str:
        """אופטימיזציה של פרומפט קיים"""
        
        optimization_prompt = f"""
        Optimize the following prompt for {optimization_goal}:
        
        Original prompt: {original_prompt}
        
        Provide an improved version that is:
        1. More clear and specific
        2. Structured better
        3. Likely to produce better results
        
        Return only the optimized prompt.
        """
        
        response = self.send_message(optimization_prompt)
        return response["content"][0]["text"]
        
    def analyze_performance(self) -> Dict[str, Any]:
        """ניתוח ביצועים וסטטיסטיקות"""
        
        if self.usage_stats["total_requests"] == 0:
            return {"message": "No requests made yet"}
            
        success_rate = (
            self.usage_stats["successful_requests"] / 
            self.usage_stats["total_requests"]
        ) * 100
        
        avg_tokens = (
            self.usage_stats["total_tokens"] / 
            self.usage_stats["successful_requests"]
            if self.usage_stats["successful_requests"] > 0 else 0
        )
        
        return {
            "total_requests": self.usage_stats["total_requests"],
            "success_rate": f"{success_rate:.2f}%",
            "average_tokens_per_request": avg_tokens,
            "total_tokens": self.usage_stats["total_tokens"],
            "estimated_cost": f"${self.usage_stats['total_cost']:.4f}",
            "failed_requests": self.usage_stats["failed_requests"]
        }
        
    def save_results(self, results: List[Dict], filename: str = "results.json"):
        """שמירת תוצאות לקובץ"""
        
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "model": self.config.model,
            "results": results,
            "performance": self.analyze_performance()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"Results saved to {filename}")

class WorkflowAutomation:
    """אוטומציה של workflows מורכבים"""
    
    def __init__(self, optimizer: ClaudeOptimizer):
        self.optimizer = optimizer
        self.workflows = {}
        
    def register_workflow(self, name: str, steps: List[Dict]):
        """רישום workflow חדש"""
        self.workflows[name] = steps
        
    def execute_workflow(self, name: str, context: Dict = None) -> List[Any]:
        """הרצת workflow"""
        
        if name not in self.workflows:
            raise ValueError(f"Workflow '{name}' not found")
            
        results = []
        workflow_context = context or {}
        
        for step in self.workflows[name]:
            step_type = step.get("type")
            
            if step_type == "prompt":
                result = self.optimizer.send_message(
                    step["content"].format(**workflow_context)
                )
                results.append(result)
                
            elif step_type == "batch":
                prompts = step["prompts"]
                batch_results = self.optimizer.batch_process(prompts)
                results.extend(batch_results)
                
            elif step_type == "condition":
                condition = step["condition"]
                if eval(condition, {"context": workflow_context, "results": results}):
                    sub_results = self.execute_workflow(
                        step["true_workflow"], 
                        workflow_context
                    )
                    results.extend(sub_results)
                    
        return results

class RevenueGenerator:
    """מחלקה ליצירת הכנסות"""
    
    def __init__(self, optimizer: ClaudeOptimizer):
        self.optimizer = optimizer
        self.pricing = {
            "blog_post": 50.0,
            "code_generation": 100.0,
            "data_analysis": 150.0,
            "marketing_campaign": 200.0
        }
        
    def estimate_revenue(self, 
                        service_type: str,
                        quantity: int,
                        custom_pricing: Optional[float] = None) -> Dict:
        """הערכת הכנסות פוטנציאליות"""
        
        price_per_unit = custom_pricing or self.pricing.get(service_type, 0)
        total_revenue = price_per_unit * quantity
        
        # חישוב עלויות (הערכה)
        estimated_cost = quantity * 0.10  # $0.10 per request estimate
        profit = total_revenue - estimated_cost
        margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            "service_type": service_type,
            "quantity": quantity,
            "price_per_unit": price_per_unit,
            "total_revenue": total_revenue,
            "estimated_cost": estimated_cost,
            "estimated_profit": profit,
            "profit_margin": f"{margin:.2f}%"
        }
        
    def generate_service_package(self, 
                                 package_name: str,
                                 services: List[Dict]) -> Dict:
        """יצירת חבילת שירותים"""
        
        total_value = 0
        package_details = []
        
        for service in services:
            service_type = service["type"]
            quantity = service.get("quantity", 1)
            
            # יצירת תוכן לדוגמה
            content = self.optimizer.generate_content(
                service_type,
                service.get("topic", "General"),
                service.get("requirements")
            )
            
            revenue = self.estimate_revenue(service_type, quantity)
            total_value += revenue["total_revenue"]
            
            package_details.append({
                "service": service_type,
                "quantity": quantity,
                "sample": content[:200] + "...",
                "value": revenue["total_revenue"]
            })
            
        return {
            "package_name": package_name,
            "services": package_details,
            "total_value": total_value,
            "created_at": datetime.now().isoformat()
        }

def main():
    """פונקציה ראשית לדוגמה"""
    
    # יש להגדיר את ה-API key
    API_KEY = os.getenv("CLAUDE_API_KEY", "your-api-key-here")
    
    # יצירת אופטימייזר
    optimizer = ClaudeOptimizer(API_KEY)
    
    # דוגמה לשימוש בסיסי
    try:
        # שליחת הודעה פשוטה
        response = optimizer.send_message(
            "What are the best practices for using Claude API efficiently?"
        )
        print("Response:", response["content"][0]["text"][:200])
        
        # עיבוד batch
        prompts = [
            "Generate a blog title about AI",
            "Write a Python function to sort a list",
            "Explain machine learning in simple terms"
        ]
        
        batch_results = optimizer.batch_process(prompts)
        
        # ניתוח ביצועים
        performance = optimizer.analyze_performance()
        print("\nPerformance Analysis:", json.dumps(performance, indent=2))
        
        # יצירת הכנסות
        revenue_gen = RevenueGenerator(optimizer)
        revenue_estimate = revenue_gen.estimate_revenue("blog_post", 10)
        print("\nRevenue Estimate:", json.dumps(revenue_estimate, indent=2))
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()