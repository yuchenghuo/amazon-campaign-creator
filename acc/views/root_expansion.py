import flask

import acc
from acc.views.auth import is_logged_in, get_access_token
from acc.views.sponsored_products import create_campaign_data, \
    create_ad_group_data, create_keyword_data, create_campaigns, \
    create_ad_groups, create_keywords, get_bid_recommendations, \
    create_product_ad_data, create_product_ads


def get_match_type(i, is_name):
    if i % 3 == 0:
        return 'DiscBroad' if is_name else 'broad'
    elif i % 3 == 1:
        return 'DiscPhrase' if is_name else 'phrase'
    else:
        return 'DiscExact' if is_name else 'exact'


@acc.app.route('/root_expansion_campaign/', methods=['POST'])
def root_expansion_campaign():
    """Display / route."""
    if not is_logged_in():
        return {'error': 'Not logged in'}

    get_access_token()
    status = {
        'success': False,
        'campaign_created': False,
        'ad_group_created': False,
        'product_ad_created': False,
        'bid_recommendations_received': False,
        'keyword_created': False,
        'message': '',
    }

    json_data = flask.request.get_json()
    profile_id = str(json_data.get('profile_id'))
    asin = json_data.get('asin')
    sku = json_data.get('sku')
    daily_budget = json_data.get('daily_budget')
    campaign_start_date = json_data.get('campaign_start_date').replace('-', '')
    campaign_end_date = json_data.get('campaign_end_date')
    if campaign_end_date:
        campaign_end_date = campaign_end_date.replace('-', '')
    enabled = json_data.get('enabled')
    bidding = json_data.get('bidding')
    keywords = json_data.get('keywords').split(',')
    acostarget = json_data.get('acostarget')
    predicate = bidding['adjustments'][0]['predicate']
    default_bid = float(json_data.get('default_bid'))
    max_bid = float(json_data.get('max_bid'))
    bid_adjustment = float(json_data.get('bid_adjustment')) / 100
    initial_keyword_bid = json_data.get('initial_keyword_bid')

    predicate_text = ''
    if predicate == 'placementTop':
        predicate_text = '_TOS'
    elif predicate == 'placementProductPage':
        predicate_text = '_PP'
    else:
        bidding['adjustments'] = []
    if bidding['strategy'] is None:
        bidding = None
    campaign_name = f"{asin} - SPKW_SKW - RootExpansion - T{acostarget}"
    enabled = 'enabled' if enabled else 'paused'

    n = len(keywords)
    campaign_data = [
        create_campaign_data(
            campaign_name=f'{campaign_name} - {keywords[i]}',
            targeting_type='manual',
            daily_budget=daily_budget,
            state=enabled,
            start_date=campaign_start_date,
            end_date=campaign_end_date,
            bidding=bidding,
        ) for i in range(n)
    ]
    campaigns = create_campaigns(profile_id, campaign_data)
    if not campaigns:
        return status
    status['campaign_created'] = True

    ad_group_data = [
        create_ad_group_data(
            campaign_id=campaigns[i // 3],
            name=f"{asin} - SPKW_SKW - RootExpansion_"
                 f"{get_match_type(i, True)} - "
                 f"T{acostarget} - {keywords[i // 3]}",
            default_bid=default_bid,
            state=enabled,
        ) for i in range(3 * n)
    ]
    ad_groups = create_ad_groups(profile_id, ad_group_data)
    if not ad_groups:
        return status
    status['ad_group_created'] = True

    product_ads_data = [
        create_product_ad_data(
            campaigns[i // 3],
            ad_groups[i],
            asin,
            sku,
            enabled,
        ) for i in range(3 * n)
    ]
    product_ads = create_product_ads(profile_id, product_ads_data)
    if not product_ads:
        return status
    status['product_ad_created'] = True

    recommendations_broad = get_bid_recommendations(
        profile_id, ad_groups[0], keywords, 'broad')
    recommendations_phrase = get_bid_recommendations(
        profile_id, ad_groups[0], keywords, 'phrase')
    recommendations_exact = get_bid_recommendations(
        profile_id, ad_groups[0], keywords, 'exact')

    if not recommendations_broad or not recommendations_phrase \
            or not recommendations_exact:
        return status
    status['bid_recommendations_received'] = True

    bids = []
    for recommendations in zip(recommendations_broad,
                               recommendations_phrase,
                               recommendations_exact):
        for i in range(3):
            recommendation = recommendations[i]
            if recommendation['code'] != 'SUCCESS':
                bids.append(default_bid)
            else:
                suggested_bid = recommendation['suggestedBid']
                if initial_keyword_bid == 'default':
                    bids.append(default_bid)
                elif initial_keyword_bid == 'suggested':
                    suggested = suggested_bid['suggested'] * (
                            1 + bid_adjustment)
                    bids.append(
                        suggested if suggested < max_bid else default_bid)
                elif initial_keyword_bid == 'lower':
                    range_start = suggested_bid['rangeStart'] * (
                            1 + bid_adjustment)
                    bids.append(
                        range_start if range_start < max_bid else default_bid)
                elif initial_keyword_bid == 'higher':
                    range_end = suggested_bid['rangeEnd'] * (
                            1 + bid_adjustment)
                    bids.append(
                        range_end if range_end < max_bid else default_bid)

    keyword_data = [
        create_keyword_data(
            campaign_id=campaigns[i // 3],
            ad_group_id=ad_groups[i],
            keyword_text=keywords[i // 3],
            match_type=get_match_type(i, False),
            state=enabled,
            bid=bids[i],
        ) for i in range(3 * n)
    ]
    keywords_ids = create_keywords(profile_id, keyword_data)
    if not keywords_ids:
        return status
    status['keyword_created'] = True

    if len(campaigns) == n and len(ad_groups) == 3 * n and len(
            keywords_ids) == 3 * n:
        status['success'] = True
        status['message'] = 'All campaigns are successfully created!'
        return status

    for i, campaign in enumerate(campaigns):
        if campaign == 0:
            status['message'] += f'\nCampaign with keyword "{keywords[i]}" ' \
                                 f'at position {i} is not created.'
    return status
