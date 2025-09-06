import json
from typing import Dict, Any, Optional, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema import BaseMessage
from .config import Config

class AIAnalyzer:
    """Handles AI-powered analysis using LangChain with Google Gemini."""
    
    def __init__(self, temperature: float = 0.7):
        """Initialize the AI analyzer with LangChain components."""
        self.llm = Config.get_chat_model(temperature=temperature)
        self.output_parser = StrOutputParser()
        
    def create_analysis_chain(self):
        """Create a LangChain chain for data analysis."""
        system_prompt = """You are an expert data analyst with extensive experience in statistical analysis and business intelligence. 
        Your role is to analyze dataset summaries and provide actionable insights that can drive business decisions.
        
        Please provide insights in the following format:
        1. Key Statistical Findings
        2. Data Quality Assessment
        3. Pattern Recognition
        4. Business Recommendations
        5. Areas for Further Investigation
        
        Be specific, practical, and focus on actionable insights."""
        
        human_prompt = """Analyze the following dataset summary and provide comprehensive insights:

Dataset Summary:
{data_summary}

Please provide detailed analysis covering statistical significance, data quality issues, patterns, and business recommendations."""

        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt)
        ])
        
        chain = prompt_template | self.llm | self.output_parser
        return chain
    
    def generate_insights(self, data_summary: Dict[str, Any]) -> Optional[str]:
        """
        Generate insights using LangChain with Gemini.
        
        Args:
            data_summary (Dict[str, Any]): A summary of the dataset statistics.
        
        Returns:
            Optional[str]: Generated insights or None if the analysis fails.
        """
        try:
            # Create the analysis chain
            analysis_chain = self.create_analysis_chain()
            
            # Format the data summary for better readability
            formatted_summary = json.dumps(data_summary, indent=2, default=str)
            
            # Generate insights using the chain
            insights = analysis_chain.invoke({"data_summary": formatted_summary})
            
            return insights
            
        except Exception as e:
            print(f"Error generating insights with LangChain: {e}")
            return None
    
    def generate_narrative_report(self, analysis: Dict[str, Any], 
                                viz_metadata: List[Dict], 
                                dataset_name: str, 
                                data_types: Dict[str, List]) -> Optional[str]:
        """
        Generate a comprehensive narrative report using LangChain.
        
        Args:
            analysis: Statistical analysis results
            viz_metadata: Metadata about generated visualizations
            dataset_name: Name of the dataset
            data_types: Types of columns in the dataset
            
        Returns:
            Optional[str]: Generated narrative report
        """
        try:
            system_prompt = """You are an expert data analyst creating comprehensive reports. 
            Create an engaging and insightful analysis report in markdown format that includes:
            
            1. Executive Summary
            2. Dataset Overview
            3. Statistical Analysis
            4. Visualization Insights
            5. Key Findings and Patterns
            6. Data Quality Assessment
            7. Business Recommendations
            8. Technical Recommendations
            
            Make the report professional, actionable, and easy to understand for both technical and non-technical stakeholders.
            Use markdown formatting for better readability."""
            
            human_prompt = """Create a comprehensive analysis report for the dataset with the following information:

Dataset Name: {dataset_name}

Data Types:
{data_types}

Statistical Analysis:
{analysis}

Visualizations Created:
{visualizations}

Please create a detailed markdown report that references visualizations using the format: ![Description](./filename.png)

Focus on:
- Clear explanations of findings
- Actionable business insights
- Data quality observations
- Recommendations for further analysis
- Statistical significance of patterns"""

            prompt_template = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(system_prompt),
                HumanMessagePromptTemplate.from_template(human_prompt)
            ])
            
            chain = prompt_template | self.llm | self.output_parser
            
            # Prepare the input data
            report = chain.invoke({
                "dataset_name": dataset_name,
                "data_types": json.dumps(data_types, indent=2),
                "analysis": json.dumps(analysis, indent=2, default=str),
                "visualizations": json.dumps(viz_metadata, indent=2)
            })
            
            return report
            
        except Exception as e:
            print(f"Error generating narrative report: {e}")
            return None
    
    def analyze_patterns(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Analyze patterns in the data using LangChain.
        
        Args:
            data: Data to analyze for patterns
            
        Returns:
            Optional[str]: Pattern analysis results
        """
        try:
            prompt_template = ChatPromptTemplate.from_messages([
                SystemMessage(content="""You are a pattern recognition expert. Analyze the provided data for:
                1. Trends and seasonality
                2. Correlations and relationships
                3. Anomalies and outliers
                4. Distribution patterns
                5. Business-relevant insights
                
                Provide specific, actionable insights."""),
                HumanMessage(content=f"Analyze these patterns: {json.dumps(data, indent=2, default=str)}")
            ])
            
            chain = prompt_template | self.llm | self.output_parser
            result = chain.invoke({})
            
            return result
            
        except Exception as e:
            print(f"Error in pattern analysis: {e}")
            return None
    
    def suggest_next_steps(self, analysis_results: Dict[str, Any]) -> Optional[str]:
        """
        Suggest next steps based on analysis results.
        
        Args:
            analysis_results: Results from previous analysis
            
        Returns:
            Optional[str]: Suggested next steps
        """
        try:
            system_prompt = """You are a senior data scientist providing strategic recommendations. 
            Based on the analysis results, suggest specific next steps for:
            1. Data collection improvements
            2. Further analysis opportunities
            3. Business actions to take
            4. Technical implementations
            5. Monitoring and tracking metrics
            
            Be specific and actionable."""
            
            prompt_template = ChatPromptTemplate.from_messages([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Based on these analysis results, what should be the next steps?\n\n{json.dumps(analysis_results, indent=2, default=str)}")
            ])
            
            chain = prompt_template | self.llm | self.output_parser
            suggestions = chain.invoke({})
            
            return suggestions
            
        except Exception as e:
            print(f"Error generating next steps: {e}")
            return None

# Example usage and testing
"""if __name__ == "__main__":
    # Test the AI Analyzer
    analyzer = AIAnalyzer()
    
    # Sample data for testing
    sample_data = {
        "numerical": {
            "mean": {"sales": 1500.0, "quantity": 25.0},
            "median": {"sales": 1200.0, "quantity": 20.0},
            "std_dev": {"sales": 500.0, "quantity": 10.0}
        },
        "missing_values": {"sales": 0, "quantity": 5},
        "outliers": {"sales": 12, "quantity": 3},
        "categorical": {
            "region": {"value_counts": {"North": 100, "South": 80}, "unique_values": 4}
        }
    }
    
    try:
        insights = analyzer.generate_insights(sample_data)
        if insights:
            print("Generated Insights:")
            print(insights)
        else:
            print("Failed to generate insights")
            
    except Exception as e:
        print(f"Test failed: {e}")"""