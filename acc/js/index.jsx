import React from 'react';
import MenuBar from './MenuBar';
import ProfileSelect from "./ProfileSelect";
import SingleKeyword from "./SingleKeyword";

class Index extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: false,
      profileSelected: {'profileId': 0, 'countryCode': 'N/A', 'accountInfo': {'name': 'Please Log In First'}},
    };
    this.logOut = this.logOut.bind(this);
    this.singleKeywordSubmit = this.singleKeywordSubmit.bind(this);
    this.handleProfileChange = this.handleProfileChange.bind(this);
  }

  componentDidMount() {
    fetch('/login_status/')
      .then(res => res.json())
      .then(res => {
        this.setState({
          isLoggedIn: res.logged_in === 'true'
        })
    });
  }

  logOut() {
    fetch('/logout/', {
      method: 'POST'
    }).then(() => window.location.reload())
  }

  singleKeywordSubmit(state) {
    if (this.state.isLoggedIn && this.state.profileSelected !== null) {
      fetch('/single_keyword_campaign/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          profile_id: this.state.profileSelected.profileId,
          asin: state.asin,
          sku: state.sku,
          enabled: state.enabled,
          acostarget: state.acosTarget,
          campaign_start_date: state.campaignStartDate,
          campaign_end_date: state.campaignEndDate,
          daily_budget: state.dailyBudget,
          default_bid: state.defaultBid,
          max_bid: state.maxBid,
          bid_adjustment: state.bidAdjustment,
          keywords: state.keywords,
          initial_keyword_bid: state.initialKeywordBid,
          bidding: {
            strategy: state.biddingStrategy,
            adjustments: [{
              predicate: state.adjustments,
              percentage: state.percentage,
            }]
          }
        })}
      )
        .then((res) => res.json())
        .then((res) => {
          alert(
            `Success: ${res.success}\n`
            + `Campaigns Created: ${res.campaign_created}\n`
            + `Ad Groups Created: ${res.ad_group_created}\n`
            + `Product Ads Created: ${res.product_ad_created}\n`
            + `Keywords Created: ${res.keyword_created}\n`
            + `Bid Recommendations Received: ${res.bid_recommendations_received}\n`
          );
          console.log(res);
        })
    }
  }

  handleProfileChange(profile) {
    this.setState({
      profileSelected: profile
    });
  }

  render() {
    return (
      <div id={'index-page'}>
        <MenuBar isLoggedIn={this.state.isLoggedIn} logOut={this.logOut}></MenuBar>
        <hr></hr>
        <ProfileSelect onChange={this.handleProfileChange} profileSelected={this.state.profileSelected}></ProfileSelect>
        <div style={{ marginLeft: 100 }} id={'campaignTypesSelect'}>
          <p style={{ color: "white", fontFamily: 'Anek Latin, sans-serif', fontSize: 25, fontWeight: "bold", marginBottom: 5 }}> Please Choose A Campaign Theme </p>
          <SingleKeyword onSubmit={this.singleKeywordSubmit}/>
        </div>
      </div>
    );
  }
}

export default Index;
