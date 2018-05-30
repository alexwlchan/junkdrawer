extern crate docopt;

extern crate reqwest;
extern crate serde;
extern crate serde_json;

#[macro_use]
extern crate serde_derive;


use std::io::prelude::*;
use std::io;
use std::fs::{create_dir, File};
use std::path::Path;

use docopt::Docopt;


const USAGE: &'static str = "
Download Apple TV screensavers.

Usage:
  download_atv_screensavers --dir=<DIR>
  download_atv_screensavers (-h | --help)

Options:
  -h --help     Show this screen.
  --dir=<DIR>   Directory to save the screensavers to.
";


#[derive(Deserialize)]
struct Asset {
    url: String,
    #[serde(rename = "accessibilityLabel")] accessibility_label: String,
    #[serde(rename = "timeOfDay")] time_of_day: String,
}


#[derive(Deserialize)]
struct AssetCollection {
    assets: Vec<Asset>,
}


#[derive(Deserialize)]
struct Args {
    flag_dir: String,
}


fn main() -> Result<(), serde_json::Error> {
    let download_url = "http://a1.phobos.apple.com/us/r1000/000/Features/atv/AutumnResources/videos/entries.json";

    let args: Args = Docopt::new(USAGE)
                            .and_then(|d| d.deserialize())
                            .unwrap_or_else(|e| e.exit());

    let text = reqwest::get(download_url).unwrap()
        .text().unwrap();

    let all_collections: Vec<AssetCollection> = serde_json::from_str(&text)?;

    let all_assets = all_collections.iter()
        .map(|collection| collection.assets.iter())
        .flat_map(|it| it.clone());

    let out_dir = Path::new(&args.flag_dir);
    match create_dir(out_dir) {
        Ok(_) => (),
        Err(_) => ()
    };

    let mut count = 0;
    for asset in all_assets {
        count += 1;
        print!(".");
        io::stdout().flush().unwrap();

        let extension = Path::new(&asset.url)
            .extension()
            .unwrap()
            .to_str()
            .unwrap();
        let name = format!("{:03}-{}-{}.{}", count, asset.accessibility_label, asset.time_of_day, extension);

        let out_path = out_dir.join(name);
        let mut file = File::create(out_path).unwrap();
        let mut video = reqwest::get(&asset.url).unwrap();
        video.copy_to(&mut file).unwrap();
    }

    print!("\n");
    println!("Downloaded {} videos to {}", count, args.flag_dir);

    Ok(())
}
