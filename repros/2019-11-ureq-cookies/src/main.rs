extern crate ureq;

fn main() {
    let mut agent = ureq::agent();

    agent.set("Cookie", "name=value");
    agent.set("Cookie", "name2=value2");

    let resp = agent.get("http://127.0.0.1:5000/").call();

    println!("{:?}", resp);
}
