import json

import flask
import requests


def create_campaign_data(campaign_name,
                         targeting_type,
                         daily_budget,
                         start_date,
                         premium_bid_adjustment=False,
                         campaign_type='sponsoredProducts',
                         state='enabled',
                         end_date=None,
                         bidding=None):
    campaign_data = {
        'campaign_name': campaign_name,
        'campaign_type': campaign_type,
        'targeting_type': targeting_type,
        'state': state,
        'daily_budget': daily_budget,
        'start_date': start_date,
        'premium_adjustment': premium_bid_adjustment,
        'bidding': bidding,
    }
    if end_date:
        campaign_data['end_date'] = end_date
    return campaign_data


def create_campaigns(profile_id, campaign_data):
    """Create campaign on Amazon API."""
    json_data = []
    for campaign in campaign_data:
        data = {
            'name': campaign['campaign_name'],
            'campaignType': campaign['campaign_type'],
            'targetingType': campaign['targeting_type'],
            'state': campaign['state'],
            'dailyBudget': campaign['daily_budget'],
            'startDate': campaign['start_date'],
            'endDate': campaign['end_date'],
        }

        if campaign['premium_adjustment']:
            data['premiumBidAdjustment'] = campaign['premium_adjustment']
        if campaign['bidding']:
            data['bidding'] = campaign['bidding']
        json_data.append(data)

    r = requests.post(
        'https://advertising-api.amazon.com/v2/campaigns',
        headers={
            'Amazon-Advertising-API-ClientId': flask.session['client_id'],
            'Amazon-Advertising-API-Scope': profile_id,
            'Authorization': 'Bearer ' + flask.session['access_token'],
            'Content-Type': 'application/json',
        },
        data=json.dumps(json_data),
    )
    if r.status_code == 207 and all(campaign['code'] == 'SUCCESS' for campaign in r.json()):
        return [campaign['campaignId'] for campaign in r.json()]

    return []


def create_ad_group_data(campaign_id,
                         name,
                         default_bid=0.02,
                         state='enabled'):
    return {
        'campaign_id': campaign_id,
        'default_bid': default_bid,
        'name': name,
        'state': state,
    }


def create_ad_groups(profile_id, ad_group_data):
    json_data = []
    for ad_group in ad_group_data:
        json_data.append(
            {
                'name': ad_group['name'],
                'campaignId': ad_group['campaign_id'],
                'defaultBid': ad_group['default_bid'],
                'state': ad_group['state'],
            }
        )

    r = requests.post(
        'https://advertising-api.amazon.com/v2/sp/adGroups',
        headers={
            'Amazon-Advertising-API-ClientId': flask.session['client_id'],
            'Amazon-Advertising-API-Scope': profile_id,
            'Authorization': 'Bearer ' + flask.session['access_token'],
            'Content-Type': 'application/json',
        },
        data=json.dumps(json_data),
    )

    return [ad_group['adGroupId'] for ad_group in r.json()]


def create_keyword_data(campaign_id,
                        ad_group_id,
                        keyword_text,
                        match_type,
                        state='enabled',
                        bid=None):
    return {
        'campaign_id': campaign_id,
        'ad_group_id': ad_group_id,
        'keyword_text': keyword_text,
        'match_type': match_type,
        'state': state,
        'bid': bid,
    }


def create_keywords(profile_id, keyword_data):
    json_data = []
    for keyword in keyword_data:
        json_data.append(
            {
                'keywordText': keyword['keyword_text'],
                'matchType': keyword['match_type'],
                'state': keyword['state'],
                'bid': keyword['bid'],
                'campaignId': keyword['campaign_id'],
                'adGroupId': keyword['ad_group_id'],
            }
        )

    r = requests.post(
        'https://advertising-api.amazon.com/v2/sp/keywords',
        headers={
            'Amazon-Advertising-API-ClientId': flask.session['client_id'],
            'Amazon-Advertising-API-Scope': profile_id,
            'Authorization': 'Bearer ' + flask.session['access_token'],
            'Content-Type': 'application/json',
        },
        data=json.dumps(json_data),
    )
    return [keyword['keywordId'] for keyword in r.json()]


def get_bid_recommendations(profile_id, adgroup_id, keywords, match_type):
    json_data = {
        'adGroupId': adgroup_id,
        'keywords': [],
    }
    for keyword in keywords:
        json_data['keywords'].append(
            {
                'keyword': keyword,
                'matchType': match_type,
            }
        )

    r = requests.post(
        'https://advertising-api.amazon.com/v2/sp/keywords/bidRecommendations',
        headers={
            'Amazon-Advertising-API-ClientId': flask.session['client_id'],
            'Amazon-Advertising-API-Scope': profile_id,
            'Authorization': 'Bearer ' + flask.session['access_token'],
            'Content-Type': 'application/json',
        },
        data=json.dumps(json_data),
    )
    return r.json()['recommendations']

