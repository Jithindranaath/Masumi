from app.crew import BudgetPlannerCrew
from logging_config import get_logger

# Keep the original ResearchCrew for backward compatibility
class ResearchCrew:
    def __init__(self, verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        # Use the new BudgetPlannerCrew instead
        budget_crew = BudgetPlannerCrew(verbose=verbose, logger=logger)
        self.crew = budget_crew.crew
        self.logger.info("BudgetPlannerCrew initialized via ResearchCrew")

    def create_crew(self):
        # This method is kept for compatibility but not used
        pass