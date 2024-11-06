import {MongoClient} from "mongodb";

const MONGO_URI = "mongodb://localhost:27017"

const client = await new MongoClient(MONGO_URI).connect()

const db = client.db("lnkd-llm");

export const lnkd_requests_collection = db.collection("lnkd_requests");