package repro;

import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;
import com.amazonaws.services.s3.model.StorageClass;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.time.format.DateTimeFormatter;
import java.time.LocalDateTime;

public class Repro {
    public static void main(String[] args) {
        AmazonS3 s3Client = AmazonS3ClientBuilder
            .standard()
            .withRegion("eu-west-1")
            .build();

        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd.HH-mm-ss");
        LocalDateTime now = LocalDateTime.now();

        String bucket = "wellcomecollection-storage-infra";

        String putKey = "storage-class.put." + fmt.format(now);
        String copyKey = "storage-class.copy." + fmt.format(now);

        StorageClass storageClass = StorageClass.ReducedRedundancy;

        InputStream stream = new ByteArrayInputStream(
            "Hello world".getBytes(StandardCharsets.UTF_8)
        );

        // PUT the object into S3.

        System.out.println(
            "Uploading an object to s3://" + bucket + "/" + putKey +
            " with storage class " + storageClass
        );

        PutObjectRequest putRequest =
            new PutObjectRequest(bucket, putKey, stream, new ObjectMetadata())
                .withStorageClass(StorageClass.ReducedRedundancy);

        s3Client.putObject(putRequest);
    }
}