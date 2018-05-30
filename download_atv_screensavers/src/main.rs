extern crate reqwest;
extern crate serde;
extern crate serde_json;

#[macro_use]
extern crate serde_derive;


use std::path::Path;


#[derive(Deserialize, Debug)]
struct Asset {
    url: String,
    #[serde(rename = "accessibilityLabel")] accessibility_label: String,
    #[serde(rename = "type")] asset_type: String,
    id: String,
    #[serde(rename = "timeOfDay")] time_of_day: String
}


#[derive(Deserialize, Debug)]
struct AssetCollection {
    id: String,
    assets: Vec<Asset>
}


fn main() -> Result<(), serde_json::Error> {
    let download_url = "http://a1.phobos.apple.com/us/r1000/000/Features/atv/AutumnResources/videos/entries.json";

    let text = reqwest::get(download_url).unwrap()
        .text().unwrap();

    let all_collections: Vec<AssetCollection> = serde_json::from_str(&text)?;

    let all_assets = all_collections.iter()
        .map(|collection| collection.assets.iter())
        .flat_map(|it| it.clone());;

    for (i, asset) in all_assets.enumerate() {
        let extension = Path::new(&asset.url)
            .extension()
            .unwrap()
            .to_str()
            .unwrap();
        let name = format!("{:03}-{}-{}.{}", i, asset.accessibility_label, asset.time_of_day, extension);
        println!("The name is {:?}", name);
    }

    Ok(())
}
