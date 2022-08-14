import flask

import acc
from acc.views.auth import is_logged_in, get_access_token
from acc.views.sponsored_products import create_campaign_data, \
    create_ad_group_data, create_product_target_data, create_campaigns, \
    create_ad_groups, create_product_targets, create_product_ad_data, \
    create_product_ads, \
    get_auto_target_recommendations, get_product_targets, \
    update_auto_product_targets, create_keywords, create_keyword_data


def get_targeting_group_name(i):
    if i % 4 == 0:
        return 'Close'
    elif i % 4 == 1:
        return 'Loose'
    elif i % 4 == 2:
        return 'Complementary'
    elif i % 4 == 3:
        return 'Substitute'


@acc.app.route('/auto_disaggregation_campaign/', methods=['POST'])
def auto_disaggregation_campaign():
    """Display / route."""
    if not is_logged_in():
        return {'error': 'Not logged in'}

    get_access_token()
    status = {
        'success': False,
        'campaign_created': False,
        'ad_group_created': False,
        'product_ad_created': False,
        'negative_keyword_created': False,
        'bid_recommendations_received': False,
        'product_targets_created': False,
        'negative_targets_created': False,
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
    negative_keywords_exact = json_data.get('negative_keywords_exact')
    if negative_keywords_exact:
        negative_keywords_exact = [x.strip() for x in
                                   negative_keywords_exact.split(',')]
    negative_keywords_phrase = json_data.get('negative_keywords_phrase')
    if negative_keywords_phrase:
        negative_keywords_phrase = [x.strip() for x in
                                    negative_keywords_phrase.split(',')]
    negative_asins = json_data.get('negative_asins')
    if negative_asins:
        negative_asins = [x.strip() for x in negative_asins.split(',')]
    enabled = json_data.get('enabled')
    bidding = json_data.get('bidding')
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
    campaign_name = f"{asin} - SP - A{predicate_text} - T{acostarget}"
    enabled = 'enabled' if enabled else 'paused'

    n = 4
    campaign_data = [
        create_campaign_data(
            campaign_name=f'{campaign_name} - {get_targeting_group_name(i)}',
            targeting_type='auto',
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
    print(campaigns)
    status['campaign_created'] = True

    ad_group_data = [
        create_ad_group_data(
            campaign_id=campaigns[i],
            name=campaign_name,
            default_bid=default_bid,
            state=enabled,
        ) for i in range(n)
    ]
    ad_groups = create_ad_groups(profile_id, ad_group_data)
    if not ad_groups:
        return status
    status['ad_group_created'] = True

    product_ads_data = [
        create_product_ad_data(
            campaigns[i],
            ad_groups[i],
            asin,
            sku,
            enabled,
        ) for i in range(n)
    ]
    product_ads = create_product_ads(profile_id, product_ads_data)
    if not product_ads:
        return status
    status['product_ad_created'] = True

    keyword_data = []
    for i in range(len(negative_keywords_exact)):
        keyword_data.append(create_keyword_data(
            campaign_id=campaigns[i],
            ad_group_id=ad_groups[i],
            keyword_text=negative_keywords_exact[i],
            match_type='negativeExact',
            state=enabled,
        ))
    for i in range(len(negative_keywords_phrase)):
        keyword_data.append(create_keyword_data(
            campaign_id=campaigns[i],
            ad_group_id=ad_groups[i],
            keyword_text=negative_keywords_phrase[i],
            match_type='negativePhrase',
            state=enabled,
        ))
    negative_keywords = create_keywords(profile_id, keyword_data, True) \
        if keyword_data else []
    if keyword_data and not negative_keywords:
        return status
    status['negative_keyword_created'] = True

    targets_data = [
        create_product_target_data(
            campaigns[i],
            ad_groups[i],
            negative_asins[i],
            enabled,
        ) for i in range(len(negative_asins))
    ]
    negative_targets = create_product_targets(profile_id, targets_data, True) \
        if targets_data else []
    if targets_data and not negative_targets:
        return status
    status['negative_targets_created'] = True

    recommendations = get_auto_target_recommendations(profile_id, ad_groups)
    if not recommendations:
        return status
    status['bid_recommendations_received'] = True

    bids = []
    for recommendation in recommendations:
        recommendation = recommendation[0]
        if recommendation['code'] != 'SUCCESS':
            bids.append(default_bid)
            continue
        suggested_bid = recommendation['suggestedBid']
        if initial_keyword_bid == 'default':
            bids.append(default_bid)
        elif initial_keyword_bid == 'suggested':
            suggested = suggested_bid['suggested'] * (1 + bid_adjustment)
            bids.append(suggested if suggested < max_bid else default_bid)
        elif initial_keyword_bid == 'lower':
            range_start = suggested_bid['rangeStart'] * (1 + bid_adjustment)
            bids.append(range_start if range_start < max_bid else default_bid)
        elif initial_keyword_bid == 'higher':
            range_end = suggested_bid['rangeEnd'] * (1 + bid_adjustment)
            bids.append(range_end if range_end < max_bid else default_bid)

    target_ids = get_product_targets(profile_id, campaigns)
    if not update_auto_product_targets(profile_id, target_ids, bids):
        return status

    if 0 not in campaigns and 0 not in ad_groups:
        status['success'] = True
        status['message'] = 'All campaigns are successfully created!'
        return status

    for i, campaign in enumerate(campaigns):
        if campaign == 0:
            status['message'] += f'\nCampaign with product target ' \
                                 f'"{get_targeting_group_name(i)}" ' \
                                 f'at position {i} ' \
                                 f'is not created.'
    return status
