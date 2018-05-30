extern crate reqwest;

fn main() {
    let text = reqwest::get("https://www.rust-lang.org")
        .unwrap()
        .text()
        .unwrap();
    println!("text = {:?}", text);
}
