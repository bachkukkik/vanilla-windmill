from datetime import datetime, timedelta
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
import json
import pandas as pd
import pytz
import wmill

def main(
    lookback: int = 1, 
    date_start: str = "", 
    date_end: str = "", 
    fb_path_credentials: str = "u/krichkorn/json_fb_app_uxible_ads_mngmt"
):
    # retrieve variables, resources, states using the wmill client
    try:
        creds = json.loads(wmill.get_variable(fb_path_credentials))
        assert creds.get("app_id"), "Please provide `app_id` in json"
        assert creds.get("app_secret"), "Please provide `app_secret` in json"
        assert creds.get("access_token"), "Please provide `access_token` in json"
        assert creds.get("ad_account"), "Please provide `ad_account` in json"

    except Exception as e:
        raise e

    else:
        FacebookAdsApi.init(creds.get("app_id"), creds.get("app_secret"), creds.get("access_token"))
        my_account = AdAccount(creds.get("ad_account"))

    if not lookback:
        lookback = 1

    if not date_start:
        date_start = (datetime.now(tz=pytz.timezone("Asia/Bangkok")) - timedelta(days=lookback)).strftime("%Y-%m-%d")
    
    if not date_end:
        date_end = datetime.now(tz=pytz.timezone("Asia/Bangkok")).strftime("%Y-%m-%d")

    # Get insights for the specified date range and breakdown by day
    insights = my_account.get_insights(
        fields=[
            AdsInsights.Field.campaign_id,
            AdsInsights.Field.adset_id,
            AdsInsights.Field.ad_id,
            AdsInsights.Field.campaign_name,
            AdsInsights.Field.adset_name,
            AdsInsights.Field.ad_name,
            AdsInsights.Field.reach,
            AdsInsights.Field.impressions,
            AdsInsights.Field.unique_clicks,
            AdsInsights.Field.clicks,
            AdsInsights.Field.inline_link_clicks,
            AdsInsights.Field.inline_post_engagement,
            AdsInsights.Field.instant_experience_outbound_clicks,
            AdsInsights.Field.interactive_component_tap,
            AdsInsights.Field.conversions,
            AdsInsights.Field.spend,
            AdsInsights.Field.cpc,
            AdsInsights.Field.cpm,
            AdsInsights.Field.ctr,
            AdsInsights.Field.conversions,
            AdsInsights.Field.dda_results,
            AdsInsights.Field.date_start,
            AdsInsights.Field.date_stop,
        ],
        params={
            'time_range': {
                'since': date_start,
                'until': date_end
            },
            'time_increment': 1,  # Break down by day
            'level': 'ad',  # Can be 'campaign', 'adset', or 'ad'
        }
    )

    # Fetch all pages (in case there is pagination)
    all_insights = []
    all_insights.extend(insights)

    cols_numeric = [
        'reach', 'impressions', 'unique_clicks', 'clicks', 'inline_link_clicks', 
        'inline_post_engagement', 'spend', 'cpc', 'cpm', 'ctr', 'dda_results'
    ]
    cols_datetime = ["date_start", "date_stop"]

    df_ads = pd.DataFrame([insight.__dict__["_json"] for insight in all_insights])
    df_ads = df_ads.apply(
        lambda x: pd.to_numeric(x.fillna(0), errors="coerce") if x.name in cols_numeric else 
        pd.to_datetime(x, errors="coerce") if x.name in cols_datetime else x
    )

    return df_ads.to_dict(orient="records")