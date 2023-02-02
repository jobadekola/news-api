from cxone.endpoints.admin_api.base import BaseAdminEndpoint
from datetime import datetime
from typing import Optional
import numpy as np


class Agents(BaseAdminEndpoint):
    # https://developer.niceincontact.com/API/AdminAPI#/Agents/get-agents
    endpoint = '/agents'
    table_name = 'agent'
    
    allowed_params: Optional[dict] = {
        'updatedSince': datetime,
        'isActive': bool,
        'searchString': str,
        'fields': str,
        'skip': int,
        'top': int,
        'orderBy': str
    }
    required_params: Optional[list] = None
    default_params: Optional[dict] = {'top': 10000}

    @property
    def ids(self):
        responses = self.get_responses()
        responses = [response for response in responses if response.ok]
        
        # retrieve unique agent ids from response
        responses_json = [response.json() for response in responses]
        ids = [int(agent.get('agentId')) for response_json in responses_json for agent in response_json.get('agents')]
        return [int(id) for id in np.unique(ids)]


class AgentsSkillData(BaseAdminEndpoint):
    # https://developer.niceincontact.com/API/AdminAPI#/Agents/Agent%20Skill%20Data
    # NOTE, this endpoint returns summary data
    endpoint = '/agents/skill-data'
    table_name = 'agent_skill_data'

    allowed_params: Optional[dict] = {
        'startDate': datetime,
        'endDate': str
    }
    required_params: Optional[list] = ['startDate', 'endDate']