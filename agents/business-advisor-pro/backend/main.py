from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import random
import datetime
import json

app = FastAPI(title="Business Advisor Pro Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BusinessQuery(BaseModel):
    query: str
    business_type: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None

class BusinessAdvice(BaseModel):
    advice: str
    category: str
    action_items: List[str]
    metrics_to_track: List[str]
    risk_level: str
    confidence_score: float

class BusinessAdvisorPro:
    def __init__(self):
        self.name = "Business Advisor Pro"
        self.expertise = "Strategic business consulting and growth advisory"
        self.experience_years = 25
        
        self.business_categories = {
            "strategy": {
                "keywords": ["strategy", "planning", "roadmap", "vision", "mission", "goals"],
                "responses": [
                    "Let's develop a comprehensive strategic framework that aligns with your market position.",
                    "I recommend a three-phase strategic approach focusing on immediate wins and long-term sustainability.",
                    "Your strategic roadmap should balance innovation with operational excellence.",
                    "Consider implementing OKRs (Objectives and Key Results) to measure strategic progress."
                ]
            },
            "finance": {
                "keywords": ["revenue", "profit", "cash flow", "funding", "investment", "budget", "cost"],
                "responses": [
                    "Your financial strategy needs to focus on sustainable cash flow generation and working capital optimization.",
                    "I suggest implementing zero-based budgeting to identify cost optimization opportunities.",
                    "Consider diversifying revenue streams to reduce dependency on single income sources.",
                    "Your unit economics show potential for improvement in customer acquisition cost efficiency."
                ]
            },
            "marketing": {
                "keywords": ["marketing", "customers", "brand", "sales", "acquisition", "conversion"],
                "responses": [
                    "Your marketing strategy should focus on customer lifetime value optimization rather than just acquisition.",
                    "I recommend implementing a data-driven attribution model to optimize marketing spend allocation.",
                    "Consider developing a content-first approach to build brand authority in your industry.",
                    "Your customer acquisition funnel needs optimization at the awareness and consideration stages."
                ]
            },
            "operations": {
                "keywords": ["operations", "efficiency", "process", "automation", "productivity", "scale"],
                "responses": [
                    "Operational excellence requires systematic process documentation and continuous improvement.",
                    "I suggest implementing lean methodology to eliminate waste and improve efficiency.",
                    "Consider automation for repetitive tasks to free up resources for strategic initiatives.",
                    "Your operations should be designed for scalability from day one."
                ]
            },
            "team": {
                "keywords": ["team", "hiring", "culture", "management", "leadership", "employee"],
                "responses": [
                    "Building a high-performance culture starts with clear values and accountability systems.",
                    "I recommend implementing regular 360-degree feedback and performance review cycles.",
                    "Your hiring strategy should prioritize cultural fit alongside technical competency.",
                    "Consider implementing employee stock option plans to align team incentives with company growth."
                ]
            },
            "growth": {
                "keywords": ["growth", "expansion", "scale", "market", "competition", "opportunity"],
                "responses": [
                    "Sustainable growth requires a balance between market expansion and operational efficiency.",
                    "I suggest conducting thorough market analysis before entering new segments or geographies.",
                    "Your growth strategy should be metrics-driven with clear success criteria and exit conditions.",
                    "Consider partnerships and strategic alliances to accelerate market penetration."
                ]
            }
        }
        
        self.industry_insights = {
            "technology": {
                "trends": ["AI/ML adoption", "Cloud transformation", "Cybersecurity", "Remote work tech"],
                "challenges": ["Talent shortage", "Rapid obsolescence", "Security threats", "Scaling costs"],
                "opportunities": ["Automation", "Data monetization", "Platform economics", "Global markets"]
            },
            "retail": {
                "trends": ["E-commerce growth", "Omnichannel experience", "Sustainability", "Personalization"],
                "challenges": ["Supply chain disruption", "Margin pressure", "Consumer behavior shifts"],
                "opportunities": ["Direct-to-consumer", "Subscription models", "Social commerce"]
            },
            "healthcare": {
                "trends": ["Telemedicine", "Personalized medicine", "AI diagnostics", "Preventive care"],
                "challenges": ["Regulatory compliance", "Data privacy", "Cost containment"],
                "opportunities": ["Digital health", "Wearable tech", "Remote monitoring"]
            },
            "finance": {
                "trends": ["Fintech disruption", "Digital banking", "Cryptocurrency", "RegTech"],
                "challenges": ["Regulatory changes", "Cybersecurity", "Customer trust"],
                "opportunities": ["Open banking", "Robo-advisors", "Blockchain applications"]
            }
        }
        
        self.risk_factors = {
            "low": ["Market research", "Competitive analysis", "Team training"],
            "medium": ["New product launch", "Market expansion", "Technology adoption"],
            "high": ["Major pivot", "Large investment", "Regulatory changes"]
        }

    def analyze_business_query(self, query: str, business_type: str = None, industry: str = None) -> BusinessAdvice:
        query_lower = query.lower()
        
        # Determine category
        category = "general"
        relevant_responses = []
        
        for cat, data in self.business_categories.items():
            if any(keyword in query_lower for keyword in data["keywords"]):
                category = cat
                relevant_responses = data["responses"]
                break
        
        if not relevant_responses:
            relevant_responses = [
                "Based on your query, I recommend a comprehensive analysis of your current business model.",
                "Let's break down your challenge into actionable components with measurable outcomes.",
                "I suggest implementing a structured approach to address this business opportunity.",
                "Your situation requires strategic thinking combined with tactical execution."
            ]
        
        # Generate specific advice
        base_advice = random.choice(relevant_responses)
        
        # Add industry-specific insights
        industry_insight = ""
        if industry and industry.lower() in self.industry_insights:
            industry_data = self.industry_insights[industry.lower()]
            trend = random.choice(industry_data["trends"])
            opportunity = random.choice(industry_data["opportunities"])
            industry_insight = f" Given the {industry} industry trends, particularly {trend}, consider leveraging {opportunity} as a strategic advantage."
        
        advice = base_advice + industry_insight
        
        # Generate action items based on category
        action_items = self.generate_action_items(category, query_lower)
        
        # Generate metrics to track
        metrics = self.generate_metrics(category)
        
        # Determine risk level
        risk_level = self.assess_risk_level(query_lower)
        
        # Calculate confidence score
        confidence_score = self.calculate_confidence(query_lower, category)
        
        return BusinessAdvice(
            advice=advice,
            category=category,
            action_items=action_items,
            metrics_to_track=metrics,
            risk_level=risk_level,
            confidence_score=confidence_score
        )
    
    def generate_action_items(self, category: str, query: str) -> List[str]:
        action_templates = {
            "strategy": [
                "Conduct SWOT analysis within 2 weeks",
                "Define 3-year strategic vision and annual milestones",
                "Implement quarterly business reviews with stakeholders",
                "Establish strategic KPIs and tracking mechanisms"
            ],
            "finance": [
                "Create 13-week cash flow forecast",
                "Implement monthly financial reporting dashboard",
                "Review and optimize payment terms with suppliers",
                "Establish financial controls and approval processes"
            ],
            "marketing": [
                "Conduct customer persona research and validation",
                "Implement marketing attribution tracking",
                "Develop content calendar for next quarter",
                "A/B testing framework for all marketing campaigns"
            ],
            "operations": [
                "Document core business processes",
                "Implement process automation for repetitive tasks",
                "Establish quality metrics and monitoring",
                "Create operational efficiency dashboard"
            ],
            "team": [
                "Define company values and cultural principles",
                "Implement regular team feedback sessions",
                "Create employee development and training programs",
                "Establish clear role definitions and career paths"
            ],
            "growth": [
                "Analyze market size and competition landscape",
                "Develop growth experiment framework",
                "Create customer success and retention programs",
                "Establish partnerships and channel strategy"
            ]
        }
        
        base_actions = action_templates.get(category, [
            "Analyze current situation and define clear objectives",
            "Research industry best practices and benchmarks",
            "Create implementation timeline with milestones",
            "Establish success metrics and review processes"
        ])
        
        return random.sample(base_actions, min(3, len(base_actions)))
    
    def generate_metrics(self, category: str) -> List[str]:
        metrics_by_category = {
            "strategy": ["Market share growth", "Strategic initiative completion rate", "Competitive positioning score"],
            "finance": ["Monthly recurring revenue", "Cash burn rate", "Customer acquisition cost", "Lifetime value"],
            "marketing": ["Customer acquisition cost", "Conversion rates", "Brand awareness metrics", "Lead quality score"],
            "operations": ["Process efficiency ratio", "Error rates", "Automation adoption", "Productivity metrics"],
            "team": ["Employee satisfaction score", "Retention rate", "Performance review scores", "Training completion"],
            "growth": ["Monthly growth rate", "Market penetration", "Customer expansion revenue", "Churn rate"]
        }
        
        return metrics_by_category.get(category, ["ROI", "Customer satisfaction", "Operational efficiency", "Revenue growth"])
    
    def assess_risk_level(self, query: str) -> str:
        high_risk_indicators = ["pivot", "investment", "expansion", "new market", "major change"]
        medium_risk_indicators = ["growth", "hiring", "technology", "process change"]
        
        if any(indicator in query for indicator in high_risk_indicators):
            return "high"
        elif any(indicator in query for indicator in medium_risk_indicators):
            return "medium"
        else:
            return "low"
    
    def calculate_confidence(self, query: str, category: str) -> float:
        # Base confidence based on query clarity and category match
        base_confidence = 0.7
        
        # Boost confidence for specific categories and clear queries
        if len(query.split()) > 5:  # More detailed query
            base_confidence += 0.1
        
        if category != "general":  # Matched specific category
            base_confidence += 0.15
        
        return min(0.95, base_confidence + random.uniform(-0.05, 0.1))

# Initialize the Business Advisor
business_advisor = BusinessAdvisorPro()

@app.get("/")
async def root():
    return {
        "agent": "Business Advisor Pro",
        "version": "1.0.0",
        "description": "Professional business consulting and strategic advisory AI agent",
        "expertise": [
            "Strategic Planning & Execution",
            "Financial Analysis & Optimization",
            "Marketing Strategy & Growth",
            "Operations & Process Improvement",
            "Team Building & Management",
            "Market Analysis & Competitive Intelligence"
        ],
        "experience": f"{business_advisor.experience_years} years of business consulting",
        "endpoints": {
            "/analyze": "POST - Get business advice and analysis",
            "/industry-insights": "GET - Get industry-specific insights",
            "/business-health": "POST - Comprehensive business health check",
            "/trends": "GET - Current business trends and opportunities"
        }
    }

@app.post("/analyze", response_model=BusinessAdvice)
async def analyze_business(query: BusinessQuery):
    try:
        advice = business_advisor.analyze_business_query(
            query.query, 
            query.business_type, 
            query.industry
        )
        return advice
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing business query: {str(e)}")

@app.get("/industry-insights")
async def get_industry_insights(industry: str = None):
    if industry and industry.lower() in business_advisor.industry_insights:
        return {
            "industry": industry,
            "insights": business_advisor.industry_insights[industry.lower()],
            "recommendation": f"Focus on leveraging {random.choice(business_advisor.industry_insights[industry.lower()]['opportunities'])} while mitigating {random.choice(business_advisor.industry_insights[industry.lower()]['challenges'])}"
        }
    else:
        return {
            "available_industries": list(business_advisor.industry_insights.keys()),
            "message": "Specify an industry parameter to get detailed insights"
        }

@app.post("/business-health")
async def business_health_check(business_data: Dict):
    areas = ["Strategy", "Finance", "Operations", "Marketing", "Team", "Growth"]
    health_scores = {area: random.uniform(60, 95) for area in areas}
    
    recommendations = []
    for area, score in health_scores.items():
        if score < 70:
            recommendations.append(f"Immediate attention needed in {area} - Score: {score:.1f}/100")
        elif score < 80:
            recommendations.append(f"Improvement opportunity in {area} - Score: {score:.1f}/100")
    
    overall_score = sum(health_scores.values()) / len(health_scores)
    
    return {
        "overall_health_score": round(overall_score, 1),
        "area_scores": health_scores,
        "recommendations": recommendations,
        "priority_actions": [
            "Focus on lowest scoring areas first",
            "Implement quarterly health check reviews",
            "Set improvement targets for each area"
        ],
        "next_review_date": (datetime.datetime.now() + datetime.timedelta(days=90)).strftime("%Y-%m-%d")
    }

@app.get("/trends")
async def get_business_trends():
    current_trends = [
        "AI and Automation Integration",
        "Sustainability and ESG Focus",
        "Remote and Hybrid Work Models",
        "Customer Experience Optimization",
        "Data-Driven Decision Making",
        "Agile Business Operations",
        "Digital Transformation Acceleration",
        "Subscription and Recurring Revenue Models"
    ]
    
    return {
        "current_trends": current_trends,
        "impact_analysis": {
            trend: f"High impact on {random.choice(['operations', 'revenue', 'customer satisfaction', 'market position'])}"
            for trend in random.sample(current_trends, 4)
        },
        "recommendation": "Evaluate which trends align with your business model and customer needs for strategic implementation."
    }

@app.get("/consultation-areas")
async def get_consultation_areas():
    return {
        "strategic_planning": {
            "description": "Long-term vision, market positioning, competitive strategy",
            "typical_duration": "3-6 months",
            "expected_outcomes": ["Clear strategic roadmap", "Market analysis", "Competitive advantages"]
        },
        "financial_optimization": {
            "description": "Cash flow management, profitability analysis, cost optimization",
            "typical_duration": "2-4 months", 
            "expected_outcomes": ["Improved margins", "Better cash flow", "Cost reduction strategies"]
        },
        "growth_acceleration": {
            "description": "Market expansion, customer acquisition, revenue optimization",
            "typical_duration": "4-8 months",
            "expected_outcomes": ["Increased revenue", "Market expansion", "Customer growth"]
        },
        "operational_excellence": {
            "description": "Process improvement, automation, efficiency optimization",
            "typical_duration": "2-5 months",
            "expected_outcomes": ["Improved efficiency", "Reduced errors", "Streamlined operations"]
        }
    }

if __name__ == "__main__":
    print("💼 Starting Business Advisor Pro Agent...")
    print("📊 Ready to provide strategic business consulting and advisory services!")
    uvicorn.run(app, host="0.0.0.0", port=8006)
