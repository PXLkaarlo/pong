struct Player {
    username: String,
    score: u64,
}

fn main() -> Result<(), std::io::Error> {
    let responder = zmq::Context::new().socket(zmq::REP).unwrap();
    responder.bind("tcp://127.0.0.1:696969")?;

    let mut leaderboard: Vec<Player> = Vec::new();
    let mut msg = zmq::Message::new();
    loop {
        responder.recv(&mut msg, 0).unwrap();
        if msg.as_str() == Some("get") {
            for player in &leaderboard {
                println!("{}", player.username);
                println!("{}", player.score);
            }
        } else {
            let msg: Vec<&str> = msg.as_str().unwrap().split(" ").collect();
            leaderboard.push(Player {
                username: String::from(msg[0]),
                score: msg[1].parse().unwrap(),
            });
        }
        responder.send("done", 0).unwrap();
    }
}
