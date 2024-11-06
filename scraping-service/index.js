import { LinkedInScraper } from "./linkedin.js";
import { connect } from 'amqplib/callback_api';
import { lnkd_requests_collection } from "./mongodb.js";

/**
 * 
 * @param {string} userid 
 * @param {string} password 
 * @param {string} targetProfileId 
 */
async function scrape(userid, password, targetProfileId) {
    let ob = new LinkedInScraper()
    await ob.initialise();
    try {
        let page = await ob.login(userid, password)
        let meta = await ob.fetchProfileMetadata(page, targetProfileId)
        // console.log("meta", meta);
        let posts = await ob.fetchLatest5Posts(page, targetProfileId)
        // console.log("posts", posts);
        return {meta, posts};
    } catch (err) {
        throw err;
    } finally {
        await ob.close();
    }
}

/**
 * 
 * @param {string} lnkd_request_id 
 */
async function getItemFromDB(lnkd_request_id) {
    let doc = await lnkd_requests_collection.findOneAndUpdate({
        lnkd_request_id,
        status: 1
    }, {
        $set: {
            status: 2,
            status_message: "Scraping Profile and Posts"
        },
    }, {
        returnDocument: "after",
        upsert: false
    })
    if (doc == null) {
        throw Error(`Entry not found in db for lnkd_request_id=${lnkd_request_id}`)
    }
    return doc;
}

/**
 * 
 * @param {import("amqplib/callback_api").Channel} channel 
 * @param {string} queue 
 * @param {import("amqplib").Message} msg 
 */
async function callback(channel, queue, msg) {
    let message_content, db_doc;
    try {
        message_content = msg.content.toString();
        console.log(" [x] Received %s", message_content);
        db_doc = await getItemFromDB(message_content);
    }
    catch(err) {
        console.error("Some error occured");
        console.error(err);
        channel.reject(msg, true);
        return "Failed";
    }
    let success = "Failed"
    try {
        let {meta, posts} = await scrape(db_doc.lnkd_username, db_doc.lnkd_password, db_doc.tagret_profile);
        await lnkd_requests_collection.updateOne({
            lnkd_request_id: message_content
        }, {
            $set: {
                status: 3,
                status_message: "Queued Prompt",
                posts,
                target_headline: meta.headline,
                target_name: meta.name,
                target_about: meta.about
            }
        })
        success = "Sucess"
        channel.ack(msg);
    } catch(err) {
        console.error("Some error occured when scraping");
        console.error(err);
        channel.reject(msg, true);
    }
    return success;
}

connect('amqp://localhost', function (error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(function (error1, channel) {
        if (error1) {
            throw error1;
        }
        var queue = 'scraping_queue';

        channel.assertQueue(queue, {
            durable: false
        });

        channel.prefetch(2);

        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);
        channel.consume(queue, function (msg) {
            callback(channel, queue, msg).then(console.log).catch(console.error);
        }, {
            noAck: false
        });
    });
});